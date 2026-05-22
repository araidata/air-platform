from app.models.enums import FindingStatus, ScoreDomain
from app.scoring.scoring_rules import (
    DomainCalculation,
    ExplanationDraft,
    ScoringContext,
    calculate_finding_impact,
    evidence_text,
    finding_explanation,
    matching_findings,
    score_from_explanations,
)


def calculate(context: ScoringContext) -> DomainCalculation:
    domain = ScoreDomain.privacy.value
    explanations: list[ExplanationDraft] = []

    active_privacy_findings = []
    for finding in matching_findings(context, domain):
        impact, reason = calculate_finding_impact(finding, score_domain=domain, today=context.today)
        if impact:
            explanations.append(
                finding_explanation(
                    finding,
                    score_domain=domain,
                    impact=impact,
                    reason=reason,
                )
            )
            if finding.status not in {FindingStatus.closed.value, FindingStatus.false_positive.value}:
                active_privacy_findings.append(finding)

    text = evidence_text(context)
    if context.system.uses_pii and not any(term in text for term in ["privacy", "retention", "redaction", "pii"]):
        explanations.append(
            ExplanationDraft(
                explanation_type="evidence_gap",
                title="PII governance evidence missing",
                description="The system uses PII, but no privacy, retention, redaction, or PII evidence is linked to the current record.",
                impact_value=-8,
            )
        )
    if context.system.uses_phi:
        explanations.append(
            ExplanationDraft(
                explanation_type="system_modifier",
                title="PHI sensitivity",
                description="The system uses PHI, so privacy controls require stronger evidence and review.",
                impact_value=-4,
            )
        )
    if context.system.uses_cjis:
        explanations.append(
            ExplanationDraft(
                explanation_type="system_modifier",
                title="CJIS privacy sensitivity",
                description="The system handles CJIS-adjacent records, increasing privacy review expectations.",
                impact_value=-4,
            )
        )
    if not active_privacy_findings and any(term in text for term in ["privacy", "retention", "redaction", "pii"]):
        explanations.append(
            ExplanationDraft(
                explanation_type="remediation_credit",
                title="Privacy evidence present",
                description="Linked privacy or retention evidence supports the current privacy score.",
                impact_value=2,
            )
        )

    return DomainCalculation(score_domain=domain, score_value=score_from_explanations(domain, explanations), explanations=explanations)
