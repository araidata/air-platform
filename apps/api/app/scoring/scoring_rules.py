from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Iterable, Optional

from app.models.enums import FindingRetestStatus, FindingStatus, ScoreDomain
from app.models.finding import Finding

CALCULATION_VERSION = "phase3_v1"

DOMAIN_WEIGHTS: dict[str, float] = {
    ScoreDomain.security.value: 0.30,
    ScoreDomain.privacy.value: 0.20,
    ScoreDomain.bias_civil_rights.value: 0.25,
    ScoreDomain.explainability.value: 0.10,
    ScoreDomain.governance_evidence.value: 0.15,
}

SEVERITY_DEDUCTIONS: dict[str, float] = {
    "critical": 30.0,
    "high": 18.0,
    "medium": 8.0,
    "low": 3.0,
    "informational": 0.0,
}

STATUS_MULTIPLIERS: dict[str, float] = {
    FindingStatus.new.value: 1.0,
    FindingStatus.under_review.value: 1.0,
    FindingStatus.in_remediation.value: 0.75,
    FindingStatus.awaiting_retest.value: 0.55,
    FindingStatus.mitigated.value: 0.25,
    FindingStatus.risk_accepted.value: 0.20,
    FindingStatus.false_positive.value: 0.0,
    FindingStatus.closed.value: 0.0,
}

DOMAIN_CAPS: dict[str, float] = {
    ScoreDomain.security.value: 75.0,
    ScoreDomain.privacy.value: 70.0,
    ScoreDomain.bias_civil_rights.value: 75.0,
    ScoreDomain.explainability.value: 60.0,
    ScoreDomain.governance_evidence.value: 70.0,
}

FINDING_DOMAIN_MAP: dict[str, set[str]] = {
    ScoreDomain.security.value: {"security", "agent_safety", "supply_chain", "rag_integrity"},
    ScoreDomain.privacy.value: {"privacy"},
    ScoreDomain.bias_civil_rights.value: {"bias_civil_rights"},
    ScoreDomain.explainability.value: {"explainability"},
    ScoreDomain.governance_evidence.value: {"governance"},
}

DOMAIN_LABELS: dict[str, str] = {
    ScoreDomain.security.value: "Security",
    ScoreDomain.privacy.value: "Privacy",
    ScoreDomain.bias_civil_rights.value: "Bias & Civil Rights",
    ScoreDomain.explainability.value: "Explainability",
    ScoreDomain.governance_evidence.value: "Governance Evidence",
    ScoreDomain.overall_governance.value: "Overall Governance",
}


@dataclass
class ExplanationDraft:
    explanation_type: str
    title: str
    description: str
    impact_value: float
    weight: float = 1.0
    related_finding_id: Optional[str] = None


@dataclass
class DomainCalculation:
    score_domain: str
    score_value: float
    weighted_score: float = 0.0
    explanations: list[ExplanationDraft] = field(default_factory=list)


@dataclass
class ScoringContext:
    system: object
    assessment: Optional[object]
    findings: list
    evidence: list
    airb_reviews: list
    audit_events: list
    today: date


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Score weights must have a positive total")
    return {domain: value / total for domain, value in weights.items()}


def clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def score_band(value: float) -> str:
    if value >= 90:
        return "low operational risk"
    if value >= 75:
        return "moderate operational risk"
    if value >= 50:
        return "elevated operational risk"
    if value >= 25:
        return "high operational risk"
    return "critical operational risk"


def domain_label(domain: str) -> str:
    return DOMAIN_LABELS.get(domain, domain.replace("_", " ").title())


def open_findings(findings: Iterable[Finding]) -> list[Finding]:
    return [
        finding
        for finding in findings
        if finding.status
        not in {
            FindingStatus.closed.value,
            FindingStatus.false_positive.value,
        }
    ]


def matching_findings(context: ScoringContext, score_domain: str) -> list[Finding]:
    domains = FINDING_DOMAIN_MAP.get(score_domain, {score_domain})
    return [finding for finding in context.findings if finding.domain in domains]


def evidence_text(context: ScoringContext) -> str:
    parts: list[str] = []
    for item in context.evidence:
        parts.extend(
            [
                item.title or "",
                item.description or "",
                item.raw_text or "",
                " ".join(f"{key} {value}" for key, value in (item.metadata_json or {}).items()),
            ]
        )
    return " ".join(parts).lower()


def active_airb_review(context: ScoringContext):
    reviews = [review for review in context.airb_reviews if not context.assessment or review.assessment_id in {None, context.assessment.id}]
    if not reviews:
        return None
    return sorted(reviews, key=lambda review: review.updated_at, reverse=True)[0]


def calculate_finding_impact(
    finding: Finding,
    *,
    score_domain: str,
    today: date,
) -> tuple[float, str]:
    explicit_impact = 0.0
    if isinstance(finding.score_impact, dict):
        explicit_impact = abs(float(finding.score_impact.get(score_domain, 0) or 0))
        if score_domain == ScoreDomain.governance_evidence.value:
            explicit_impact = max(explicit_impact, abs(float(finding.score_impact.get("governance", 0) or 0)))

    severity_impact = SEVERITY_DEDUCTIONS.get(finding.severity, 0.0)
    impact = max(explicit_impact, severity_impact)
    impact *= STATUS_MULTIPLIERS.get(finding.status, 1.0)

    reasons: list[str] = [f"{finding.severity} severity"]
    if finding.status in {FindingStatus.in_remediation.value, FindingStatus.awaiting_retest.value}:
        reasons.append(f"{finding.status.replace('_', ' ')} reduced active impact")
    if finding.status == FindingStatus.risk_accepted.value or finding.risk_accepted:
        impact = max(impact, severity_impact * 0.2)
        reasons.append("risk accepted but still tracked")
    if finding.retest_status == FindingRetestStatus.passed.value:
        impact *= 0.25
        reasons.append("passed retest reduced impact")
    elif finding.retest_status == FindingRetestStatus.failed.value:
        impact += 5.0
        reasons.append("failed retest increased impact")
    if finding.approval_blocking and impact > 0:
        impact += 4.0
        reasons.append("approval blocking")
    if finding.due_date and finding.due_date < today and impact > 0:
        impact += 4.0
        reasons.append("overdue")

    return round(impact, 2), ", ".join(reasons)


def finding_explanation(
    finding: Finding,
    *,
    score_domain: str,
    impact: float,
    reason: str,
) -> ExplanationDraft:
    label = domain_label(score_domain)
    return ExplanationDraft(
        explanation_type="finding_impact",
        title=f"{finding.severity.title()} finding: {finding.title}",
        description=f"{finding.title} reduced the {label} Score by {impact:g} points ({reason}).",
        impact_value=-impact,
        related_finding_id=finding.id,
    )


def apply_cap(score_domain: str, explanations: list[ExplanationDraft]) -> list[ExplanationDraft]:
    cap = DOMAIN_CAPS[score_domain]
    negative_total = abs(sum(item.impact_value for item in explanations if item.impact_value < 0))
    if negative_total <= cap:
        return explanations
    explanations.append(
        ExplanationDraft(
            explanation_type="system_modifier",
            title=f"{domain_label(score_domain)} impact capped",
            description=f"{domain_label(score_domain)} deductions were capped at {cap:g} points so the score remains interpretable.",
            impact_value=negative_total - cap,
        )
    )
    return explanations


def score_from_explanations(score_domain: str, explanations: list[ExplanationDraft]) -> float:
    explanations = apply_cap(score_domain, explanations)
    return clamp_score(100.0 + sum(item.impact_value for item in explanations))
