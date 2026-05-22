from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.ai_system import AISystem
from app.models.assessment import Assessment
from app.models.assessment_profile import AssessmentProfile
from app.models.enums import AuditEventType, EvidenceType, ScannerExecutionStatus
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.scan_type import ScanType
from app.models.scanner_definition import ScannerDefinition
from app.models.scanner_result import ScannerResult
from app.models.scanner_run import ScannerRun
from app.schemas.evidence import EvidenceCreate
from app.schemas.finding import FindingCreate
from app.schemas.scanner import ScannerRunCreate
from app.scanners.adapters.base import ScannerExecutionContext
from app.scanners.adapters.garak_adapter import GarakCliAdapter
from app.scanners.adapters.mock_adapter import MockScannerAdapter
from app.scanners.normalization.finding_normalizer import (
    NORMALIZATION_VERSION,
    normalize_scanner_findings,
)
from app.services.audit_event_service import AuditEventService
from app.services.evidence_service import EvidenceService
from app.services.finding_workflow_service import FindingWorkflowService


class ScannerExecutionService:
    def __init__(self, db: Session, storage_root: str | Path | None = None):
        self.db = db
        self.audit = AuditEventService(db)
        self.storage_root = Path(storage_root or settings.scanner_storage_root)

    def create_run(self, payload: ScannerRunCreate) -> ScannerRun:
        system = self._require_system(payload.system_id)
        assessment = self._resolve_assessment(system, payload)
        scanner_definition = self._require_scanner_definition(payload.scanner_definition_id)
        scan_type = self._require_scan_type(payload.scan_type_id)
        profile = self._require_profile(payload.assessment_profile_id)
        if not scanner_definition.enabled:
            raise HTTPException(status_code=400, detail="Scanner definition is disabled")
        if not scan_type.enabled:
            raise HTTPException(status_code=400, detail="Scan type is disabled")
        if (
            scanner_definition.supported_scan_types
            and scan_type.name not in scanner_definition.supported_scan_types
        ):
            raise HTTPException(status_code=400, detail="Scanner does not support scan type")

        run = ScannerRun(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner_definition.id,
            scan_type_id=scan_type.id,
            assessment_profile_id=profile.id if profile else None,
            scanner_name=scanner_definition.scanner_name,
            scanner_version=scanner_definition.scanner_version,
            adapter_name=scanner_definition.adapter_name,
            execution_status=ScannerExecutionStatus.pending.value,
            initiated_by=payload.initiated_by,
        )
        self.db.add(run)
        self.db.flush()
        self.audit.record(
            entity_type="scanner_run",
            entity_id=run.id,
            event_type=AuditEventType.scanner_run_created,
            actor=payload.initiated_by,
            new_value=run.execution_status,
            notes=f"{scanner_definition.display_name} queued for {scan_type.display_name}",
        )
        return run

    def execute_run(self, run_id: str, *, initiated_by: str = "operator") -> ScannerRun:
        run = self.db.get(ScannerRun, run_id)
        if not run:
            raise HTTPException(status_code=404, detail="Scanner run not found")
        if run.execution_status == ScannerExecutionStatus.completed.value:
            raise HTTPException(status_code=400, detail="Scanner run already completed")

        system = self._require_system(run.system_id)
        assessment = self.db.get(Assessment, run.assessment_id)
        scanner_definition = self._require_scanner_definition(run.scanner_definition_id)
        scan_type = self._require_scan_type(run.scan_type_id)
        profile = self.db.get(AssessmentProfile, run.assessment_profile_id) if run.assessment_profile_id else None
        adapter = self._adapter_for(scanner_definition.adapter_name)

        run.execution_status = ScannerExecutionStatus.running.value
        run.started_at = datetime.utcnow()
        run.initiated_by = initiated_by
        self.audit.record(
            entity_type="scanner_run",
            entity_id=run.id,
            event_type=AuditEventType.scanner_execution_started,
            actor=initiated_by,
            new_value=run.execution_status,
            notes=f"Executing {scanner_definition.display_name}",
        )
        self.db.flush()

        context = ScannerExecutionContext(
            run_id=run.id,
            system_id=system.id,
            system_name=system.system_name,
            risk_tier=system.risk_tier,
            scan_type=scan_type.name,
            scan_domain=scan_type.domain,
            profile_name=profile.profile_name if profile else None,
            artifact_dir=str(self.storage_root / run.id),
        )

        try:
            execution_result = adapter.execute(context)
            run_dir = self.storage_root / run.id
            raw_path = self._write_json(run_dir / "raw-output.json", execution_result.raw_output)
            log_path = self._write_text(run_dir / "execution.log", execution_result.logs)
            run.raw_output_path = str(raw_path)
            run.log_path = str(log_path)
            self.audit.record(
                entity_type="scanner_run",
                entity_id=run.id,
                event_type=AuditEventType.scanner_output_preserved,
                actor=initiated_by,
                new_value=str(raw_path),
                notes="Raw scanner output and execution logs preserved.",
            )

            raw_evidence = self._create_run_evidence(
                run,
                evidence_type=EvidenceType.scanner_output,
                title=f"Raw scanner JSON for {scan_type.display_name}",
                description="Unmodified structured scanner output preserved from execution.",
                file_path=str(raw_path),
                raw_text=json.dumps(execution_result.raw_output, indent=2, sort_keys=True),
                content_type="application/json",
                created_by=initiated_by,
            )
            self._create_run_evidence(
                run,
                evidence_type=EvidenceType.raw_log,
                title=f"Execution log for {scan_type.display_name}",
                description="Scanner execution log preserved for reproducibility and failure review.",
                file_path=str(log_path),
                raw_text=execution_result.logs,
                content_type="text/plain",
                created_by=initiated_by,
            )
            self._preserve_adapter_artifacts(run, execution_result.artifacts, initiated_by)
            if execution_result.status != ScannerExecutionStatus.completed.value:
                raise RuntimeError(execution_result.error_message or "Scanner execution failed")

            parsed = adapter.parse_output(execution_result.raw_output)
            raw_findings = adapter.normalize_findings(parsed)
            normalized = normalize_scanner_findings(
                scanner_name=run.scanner_name,
                scanner_version=run.scanner_version,
                system_id=run.system_id,
                assessment_id=run.assessment_id,
                raw_findings=raw_findings,
                raw_evidence_path=str(raw_path),
            )
            self.db.add(
                ScannerResult(
                    scanner_run_id=run.id,
                    raw_result_json=execution_result.raw_output,
                    normalized={"findings": normalized, "raw_evidence_id": raw_evidence.id},
                    normalization_version=NORMALIZATION_VERSION,
                )
            )
            normalized_payload = {"findings": normalized, "raw_evidence_id": raw_evidence.id}
            normalized_path = self._write_json(run_dir / "normalized-output.json", normalized_payload)
            self._create_run_evidence(
                run,
                evidence_type=EvidenceType.scanner_output,
                title=f"Normalized scanner output for {scan_type.display_name}",
                description="Platform-normalized scanner output preserved after parsing.",
                file_path=str(normalized_path),
                raw_text=json.dumps(normalized_payload, indent=2, sort_keys=True),
                content_type="application/json",
                created_by=initiated_by,
            )
            created_findings = self._create_findings_and_evidence(
                run=run,
                normalized_findings=normalized,
                actor=initiated_by,
            )
            run.finding_count = len(created_findings)
            run.execution_status = ScannerExecutionStatus.completed.value
            run.completed_at = datetime.utcnow()
            self.audit.record(
                entity_type="scanner_run",
                entity_id=run.id,
                event_type=AuditEventType.findings_normalized,
                actor=initiated_by,
                new_value=str(run.finding_count),
                notes=f"Normalized {run.finding_count} scanner findings.",
            )
            self.audit.record(
                entity_type="scanner_run",
                entity_id=run.id,
                event_type=AuditEventType.scanner_execution_completed,
                actor=initiated_by,
                new_value=run.execution_status,
                notes="Scanner execution completed.",
            )
        except Exception as exc:
            run.execution_status = ScannerExecutionStatus.failed.value
            run.completed_at = datetime.utcnow()
            run.error_message = str(exc)
            if not run.log_path:
                run_dir = self.storage_root / run.id
                log_path = self._write_text(run_dir / "execution.log", f"scanner execution failed: {exc}")
                run.log_path = str(log_path)
                self._create_run_evidence(
                    run,
                    evidence_type=EvidenceType.raw_log,
                    title=f"Failed scanner execution log for {scan_type.display_name}",
                    description="Failure log preserved for operator review.",
                    file_path=str(log_path),
                    raw_text=f"scanner execution failed: {exc}",
                    content_type="text/plain",
                    created_by=initiated_by,
                )
            self.audit.record(
                entity_type="scanner_run",
                entity_id=run.id,
                event_type=AuditEventType.scanner_execution_failed,
                actor=initiated_by,
                new_value=run.execution_status,
                notes=str(exc),
            )
        self.db.flush()
        return run

    def recommended_scans(
        self,
        system_id: str,
        assessment_profile_id: str | None = None,
        selected_scan_type_ids: list[str] | None = None,
    ) -> dict:
        system = self._require_system(system_id)
        profile = self._require_profile(assessment_profile_id)
        selected_names: set[str] = set()
        if selected_scan_type_ids:
            selected_names = {
                scan.name
                for scan in self.db.scalars(select(ScanType).where(ScanType.id.in_(selected_scan_type_ids))).all()
            }
        scan_types = self.db.scalars(select(ScanType).where(ScanType.enabled.is_(True))).all()
        required_names = set(profile.required_scan_types if profile else [])
        optional_names = set(profile.optional_scan_types if profile else [])
        required: list[dict] = []
        optional: list[dict] = []
        for scan_type in scan_types:
            reasons: list[str] = []
            is_required = False
            if scan_type.name in required_names:
                is_required = True
                reasons.append("required by assessment profile")
            if system.risk_tier in (scan_type.required_for_risk_tiers or []):
                is_required = True
                reasons.append(f"recommended for {system.risk_tier} risk tier")
            if scan_type.name in selected_names:
                is_required = True
                reasons.append("manually selected")
            if not is_required and scan_type.name not in optional_names:
                continue
            if scan_type.name in optional_names:
                reasons.append("optional in assessment profile")
            record = {
                "scan_type": scan_type,
                "required": is_required,
                "reason": ", ".join(reasons) or "available scan",
                "available_scanners": self.available_scanners_for(scan_type.name),
            }
            if is_required:
                required.append(record)
            else:
                optional.append(record)
        return {
            "system_id": system.id,
            "risk_tier": system.risk_tier,
            "assessment_profile": profile,
            "required_scans": required,
            "optional_scans": optional,
        }

    def available_scanners_for(self, scan_type_name: str) -> list[ScannerDefinition]:
        scanners = self.db.scalars(
            select(ScannerDefinition)
            .where(
                ScannerDefinition.enabled.is_(True),
            )
            .order_by(ScannerDefinition.display_name)
        ).all()
        return [
            scanner
            for scanner in scanners
            if not scanner.supported_scan_types or scan_type_name in scanner.supported_scan_types
        ]

    def _resolve_assessment(self, system: AISystem, payload: ScannerRunCreate) -> Assessment:
        if payload.assessment_id:
            assessment = self.db.get(Assessment, payload.assessment_id)
            if not assessment:
                raise HTTPException(status_code=404, detail="Assessment not found")
            if assessment.system_id != system.id:
                raise HTTPException(status_code=400, detail="Assessment does not belong to system")
            return assessment
        assessment = Assessment(
            system_id=system.id,
            assessment_type="Scanner ecosystem assessment",
            initiated_by=payload.initiated_by,
            status="running",
            started_at=datetime.utcnow(),
            summary="Created automatically for scanner execution.",
        )
        self.db.add(assessment)
        self.db.flush()
        self.audit.record(
            entity_type="assessment",
            entity_id=assessment.id,
            event_type=AuditEventType.assessment_created,
            actor=payload.initiated_by,
            new_value=assessment.status,
            notes="Scanner execution created assessment.",
        )
        return assessment

    def _create_findings_and_evidence(
        self,
        *,
        run: ScannerRun,
        normalized_findings: list[dict],
        actor: str,
    ) -> list[Finding]:
        created: list[Finding] = []
        workflow = FindingWorkflowService(self.db)
        evidence_service = EvidenceService(self.db)
        for normalized in normalized_findings:
            finding = workflow.create(
                FindingCreate(
                    system_id=normalized["system_id"],
                    assessment_id=normalized["assessment_id"],
                    scanner_name=normalized["scanner_name"],
                    scanner_version=normalized["scanner_version"],
                    domain=normalized["domain"],
                    severity=normalized["severity"],
                    confidence=normalized["confidence"],
                    title=normalized["title"],
                    description=normalized["description"],
                    evidence_summary=normalized["evidence_summary"],
                    remediation=normalized["remediation"],
                    score_impact=normalized["score_impact"],
                    approval_blocking=normalized["approval_blocking"],
                    actor=actor,
                )
            )
            created.append(finding)
            for item in normalized.get("evidence", []):
                evidence_service.create(
                    EvidenceCreate(
                        finding_id=finding.id,
                        evidence_type=item.get("evidence_type", EvidenceType.scanner_output.value),
                        title=item.get("title", f"Scanner evidence for {finding.title}"),
                        description=item.get("description", normalized["evidence_summary"]),
                        raw_text=item.get("raw_text"),
                        content_type=item.get("content_type", "text/plain"),
                        created_by=actor,
                        metadata_json={
                            "source": "scanner_adapter",
                            "scanner_run_id": run.id,
                            "scanner_name": run.scanner_name,
                            **normalized.get("source_metadata", {}),
                        },
                    )
                )
            self.audit.record(
                entity_type="finding",
                entity_id=finding.id,
                event_type=AuditEventType.scanner_findings_created,
                actor=actor,
                new_value=run.id,
                notes=finding.title,
            )
        return created

    def _create_run_evidence(
        self,
        run: ScannerRun,
        *,
        evidence_type: EvidenceType,
        title: str,
        description: str,
        file_path: str,
        raw_text: str,
        content_type: str,
        created_by: str,
    ) -> Evidence:
        return EvidenceService(self.db).create(
            EvidenceCreate(
                assessment_id=run.assessment_id,
                system_id=run.system_id,
                evidence_type=evidence_type,
                title=title,
                description=description,
                file_path=file_path,
                raw_text=raw_text,
                content_type=content_type,
                created_by=created_by,
                hash=self._hash_text(raw_text),
                metadata_json={
                    "source": "scanner_adapter",
                    "scanner_run_id": run.id,
                    "scanner_name": run.scanner_name,
                    "adapter_name": run.adapter_name,
                },
            )
        )

    def _preserve_adapter_artifacts(
        self,
        run: ScannerRun,
        artifacts: dict,
        created_by: str,
    ) -> None:
        artifact_specs = {
            "scanner_config_path": ("Scanner execution configuration", "application/json"),
            "report_jsonl_path": ("Native scanner report JSONL", "application/jsonl"),
            "hitlog_jsonl_path": ("Native scanner hit log JSONL", "application/jsonl"),
            "html_report_path": ("Native scanner HTML report", "text/html"),
        }
        for key, (title, content_type) in artifact_specs.items():
            value = artifacts.get(key)
            if not value:
                continue
            path = Path(value)
            if not path.exists() or not path.is_file():
                continue
            raw_text = path.read_text(encoding="utf-8", errors="replace")
            self._create_run_evidence(
                run,
                evidence_type=EvidenceType.scanner_output,
                title=title,
                description=f"{title} preserved from scanner execution.",
                file_path=str(path),
                raw_text=raw_text,
                content_type=content_type,
                created_by=created_by,
            )

    def _adapter_for(self, adapter_name: str):
        if adapter_name == "mock_adapter":
            return MockScannerAdapter()
        if adapter_name == "garak_cli_adapter":
            return GarakCliAdapter()
        raise HTTPException(status_code=400, detail=f"Adapter is not implemented: {adapter_name}")

    def _write_json(self, path: Path, payload: dict) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return path

    def _write_text(self, path: Path, payload: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
        return path

    def _hash_text(self, value: str) -> str:
        return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"

    def _require_system(self, system_id: str) -> AISystem:
        system = self.db.get(AISystem, system_id)
        if not system:
            raise HTTPException(status_code=404, detail="System not found")
        return system

    def _require_scanner_definition(self, scanner_definition_id: str) -> ScannerDefinition:
        scanner_definition = self.db.get(ScannerDefinition, scanner_definition_id)
        if not scanner_definition:
            raise HTTPException(status_code=404, detail="Scanner definition not found")
        return scanner_definition

    def _require_scan_type(self, scan_type_id: str) -> ScanType:
        scan_type = self.db.get(ScanType, scan_type_id)
        if not scan_type:
            raise HTTPException(status_code=404, detail="Scan type not found")
        return scan_type

    def _require_profile(self, assessment_profile_id: str | None) -> AssessmentProfile | None:
        if not assessment_profile_id:
            return None
        profile = self.db.get(AssessmentProfile, assessment_profile_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Assessment profile not found")
        return profile
