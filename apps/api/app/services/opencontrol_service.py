from __future__ import annotations

from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.framework_mapping import FrameworkMapping


DEFAULT_CONTROL_MAP = {
    "security": [
        ("NIST AI RMF", "MAP 5.1", "AI system security risks are identified and documented."),
        ("OWASP LLM Top 10", "LLM01", "Prompt injection and adversarial manipulation are assessed."),
        ("OpenControl", "ai-assessment.security-testing", "Security scanner evidence is linked to findings."),
    ],
    "privacy": [
        ("NIST AI RMF", "MAP 2.3", "Privacy and data handling risks are documented."),
        ("OWASP LLM Top 10", "LLM02", "Sensitive information disclosure is assessed."),
        ("OpenControl", "ai-assessment.privacy-evidence", "Privacy evidence is preserved for export."),
    ],
    "bias_civil_rights": [
        ("NIST AI RMF", "MEASURE 2.11", "Fairness and bias impacts are measured."),
        ("OpenControl", "ai-assessment.fairness-testing", "Fairness test evidence is linked to findings."),
    ],
    "rag_integrity": [
        ("NIST AI RMF", "MEASURE 2.6", "Grounding and retrieval integrity are evaluated."),
        ("OWASP LLM Top 10", "LLM08", "Vector and embedding weaknesses are assessed."),
        ("OpenControl", "ai-assessment.rag-faithfulness", "RAG evidence is preserved for reporting."),
    ],
    "explainability": [
        ("NIST AI RMF", "MAP 4.1", "Decision rationale and explanation risks are documented."),
        ("OpenControl", "ai-assessment.explainability", "Explanation evidence is linked to findings."),
    ],
    "governance": [
        ("NIST AI RMF", "GOVERN 1.5", "Policies and controls are linked to operational evidence."),
        ("OpenControl", "ai-assessment.operational-review", "Assessment evidence supports human review."),
    ],
}


class OpenControlService:
    def __init__(self, db: Session):
        self.db = db

    def create_mappings_for_finding(self, finding: Finding, explicit_mappings: list[dict[str, Any]] | None = None) -> list[FrameworkMapping]:
        rows = self._mapping_rows(finding, explicit_mappings or [])
        existing = {
            (item.framework, item.control)
            for item in self.db.scalars(select(FrameworkMapping).where(FrameworkMapping.finding_id == finding.id)).all()
        }
        created: list[FrameworkMapping] = []
        for framework, control, description in rows:
            if (framework, control) in existing:
                continue
            row = FrameworkMapping(finding_id=finding.id, framework=framework, control=control, description=description)
            self.db.add(row)
            created.append(row)
        self.db.flush()
        return created

    def export_assessment(self, assessment_id: str) -> dict[str, Any]:
        findings = self.db.scalars(select(Finding).where(Finding.assessment_id == assessment_id)).all()
        evidence = self.db.scalars(select(Evidence).where(Evidence.assessment_id == assessment_id)).all()
        evidence_by_finding: dict[str, list[Evidence]] = defaultdict(list)
        for record in evidence:
            if record.finding_id:
                evidence_by_finding[record.finding_id].append(record)
        controls: dict[tuple[str, str], dict[str, Any]] = {}
        for finding in findings:
            if not finding.framework_mappings:
                self.create_mappings_for_finding(finding)
            for mapping in finding.framework_mappings:
                key = (mapping.framework, mapping.control)
                control = controls.setdefault(
                    key,
                    {
                        "standard_key": mapping.framework,
                        "control_key": mapping.control,
                        "control_name": mapping.description,
                        "narratives": [],
                    },
                )
                control["narratives"].append(
                    {
                        "finding_id": finding.id,
                        "finding_title": finding.title,
                        "severity": finding.severity,
                        "text": finding.evidence_summary,
                        "evidence": [self._evidence_ref(item) for item in evidence_by_finding.get(finding.id, [])],
                    }
                )
        return {
            "schema": "opencontrol-lite",
            "assessment_id": assessment_id,
            "components": [{"name": "AI Assessment Scanner", "controls": list(controls.values())}],
            "evidence": [self._evidence_ref(item) for item in evidence],
        }

    def _mapping_rows(self, finding: Finding, explicit: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
        rows = [
            (str(item.get("framework")), str(item.get("control")), str(item.get("description") or item.get("control")))
            for item in explicit
            if item.get("framework") and item.get("control")
        ]
        rows.extend(DEFAULT_CONTROL_MAP.get(finding.domain, DEFAULT_CONTROL_MAP["governance"]))
        return rows

    def _evidence_ref(self, evidence: Evidence) -> dict[str, Any]:
        return {
            "id": evidence.id,
            "title": evidence.title,
            "type": evidence.evidence_type,
            "file_path": evidence.file_path,
            "hash": evidence.hash,
            "scanner_run_id": evidence.metadata_json.get("scanner_run_id"),
            "scanner_name": evidence.metadata_json.get("scanner_name"),
            "trace_id": evidence.metadata_json.get("trace_id"),
            "created_at": evidence.created_at.isoformat(),
        }
