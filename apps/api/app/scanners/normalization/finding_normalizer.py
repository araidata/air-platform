from __future__ import annotations

from typing import Any

from app.models.enums import FindingConfidence, FindingDomain, FindingSeverity

NORMALIZATION_VERSION = "phase4_mock_v1"


def normalize_scanner_findings(
    *,
    scanner_name: str,
    scanner_version: str,
    system_id: str,
    assessment_id: str,
    raw_findings: list[dict[str, Any]],
    raw_evidence_path: str | None,
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for raw in raw_findings:
        domain = _enum_value(raw.get("domain"), FindingDomain, "governance")
        severity = _enum_value(raw.get("severity"), FindingSeverity, "medium")
        confidence = _enum_value(raw.get("confidence"), FindingConfidence, "unknown")
        normalized.append(
            {
                "system_id": system_id,
                "assessment_id": assessment_id,
                "scanner_name": scanner_name,
                "scanner_version": scanner_version,
                "domain": domain,
                "severity": severity,
                "confidence": confidence,
                "title": raw.get("title") or "Scanner finding",
                "description": raw.get("description") or "Scanner output normalized into a finding.",
                "evidence_summary": raw.get("evidence_summary")
                or f"Raw scanner output preserved at {raw_evidence_path}.",
                "remediation": raw.get("remediation") or "Review scanner output and document disposition.",
                "score_impact": raw.get("score_impact") or {domain: -3},
                "approval_blocking": bool(raw.get("approval_blocking", False)),
                "source_metadata": {
                    "affected_component": raw.get("affected_component"),
                    "raw_evidence_path": raw_evidence_path,
                },
                "evidence": raw.get("evidence") or [],
            }
        )
    return normalized


def _enum_value(value: Any, enum_type, fallback: str) -> str:
    candidates = {item.value for item in enum_type}
    if isinstance(value, str) and value in candidates:
        return value
    return fallback
