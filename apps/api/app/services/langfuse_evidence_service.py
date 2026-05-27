from __future__ import annotations

import hashlib
import importlib
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.models.enums import EvidenceType
from app.models.scanner_run import ScannerRun
from app.schemas.evidence import EvidenceCreate
from app.services.evidence_service import EvidenceService


class LangfuseEvidenceService:
    def __init__(self, db: Session):
        self.db = db

    def capture_scanner_trace(
        self,
        *,
        run: ScannerRun,
        artifact_dir: Path,
        raw_output: dict[str, Any],
        created_by: str,
    ):
        trace_id = str(uuid.uuid4())
        records = self._prompt_response_records(raw_output)
        manifest = {
            "trace_id": trace_id,
            "scanner_run_id": run.id,
            "assessment_id": run.assessment_id,
            "system_id": run.system_id,
            "scanner_name": run.scanner_name,
            "scanner_version": run.scanner_version,
            "created_at": datetime.utcnow().isoformat(),
            "prompt_response_count": len(records),
            "prompt_response_records": records,
            "latency_ms": self._latency_total(records),
            "cost": self._cost(raw_output),
            "langfuse": self._send_to_langfuse(trace_id, run, raw_output, records),
        }
        path = artifact_dir / "langfuse-trace.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        raw_text = json.dumps(manifest, indent=2, sort_keys=True)
        path.write_text(raw_text, encoding="utf-8")
        return EvidenceService(self.db).create(
            EvidenceCreate(
                assessment_id=run.assessment_id,
                system_id=run.system_id,
                evidence_type=EvidenceType.scanner_output,
                title=f"Trace manifest for {run.scanner_name} scanner run",
                description="Langfuse trace reference and local prompt/response trace manifest for scanner evidence.",
                file_path=str(path),
                raw_text=raw_text,
                content_type="application/json",
                created_by=created_by,
                hash=f"sha256:{hashlib.sha256(raw_text.encode('utf-8')).hexdigest()}",
                metadata_json={
                    "source": "langfuse_trace_pipeline",
                    "scanner_run_id": run.id,
                    "scanner_name": run.scanner_name,
                    "adapter_name": run.adapter_name,
                    "trace_id": trace_id,
                    "langfuse_status": manifest["langfuse"]["status"],
                    "latency_ms": manifest["latency_ms"],
                    "cost": manifest["cost"],
                },
            )
        )

    def _send_to_langfuse(self, trace_id: str, run: ScannerRun, raw_output: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, Any]:
        if not (os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")):
            return {"status": "disabled", "reason": "LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY are not configured"}
        try:
            get_client = getattr(importlib.import_module("langfuse"), "get_client")
            client = get_client()
            with client.start_as_current_observation(
                as_type="span",
                name=f"scanner-run-{run.scanner_name}",
                input={"scanner_run_id": run.id, "scanner": run.scanner_name, "scan_type": raw_output.get("scan_type")},
            ) as span:
                span.update(output={"scanner_status": raw_output.get("execution", {}).get("exit_code", "completed")})
                for index, record in enumerate(records):
                    with client.start_as_current_observation(
                        as_type="generation",
                        name=f"{run.scanner_name}-prompt-{index + 1}",
                        model=str(raw_output.get("system", {}).get("model_version") or run.scanner_name),
                        input=record.get("prompt"),
                    ) as generation:
                        generation.update(
                            output=record.get("response_text"),
                            metadata={
                                "scanner_run_id": run.id,
                                "trace_id": trace_id,
                                "latency_ms": record.get("latency_ms"),
                                "response_status": record.get("response_status"),
                            },
                        )
            client.flush()
            return {"status": "captured", "trace_id": trace_id}
        except Exception as exc:
            return {"status": "degraded", "trace_id": trace_id, "reason": str(exc)}

    def _prompt_response_records(self, raw_output: dict[str, Any]) -> list[dict[str, Any]]:
        for key in ("prompt_response_records", "adversarial_records"):
            records = raw_output.get(key)
            if isinstance(records, list):
                return [item for item in records if isinstance(item, dict)]
        records = []
        hitlog = raw_output.get("hitlog_records")
        if isinstance(hitlog, list):
            for item in hitlog:
                if isinstance(item, dict):
                    records.append({"prompt": item.get("prompt") or item.get("probe"), "response_text": json.dumps(item)})
        return records

    def _latency_total(self, records: list[dict[str, Any]]) -> float | None:
        latencies = [item.get("latency_ms") for item in records if isinstance(item.get("latency_ms"), (int, float))]
        return round(sum(float(item) for item in latencies), 2) if latencies else None

    def _cost(self, raw_output: dict[str, Any]) -> dict[str, Any] | None:
        cost = raw_output.get("cost") or raw_output.get("usage")
        return cost if isinstance(cost, dict) else None
