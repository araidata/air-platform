from app.models.enums import FindingStatus, ScoreDomain
from app.scoring.scoring_rules import (
    DomainCalculation,
    ExplanationDraft,
    ScoringContext,
    calculate_finding_impact,
    finding_explanation,
    matching_findings,
    score_from_explanations,
)


def calculate(context: ScoringContext) -> DomainCalculation:
    domain = ScoreDomain.security.value
    explanations: list[ExplanationDraft] = []

    active_security_findings = []
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
                active_security_findings.append(finding)

    if active_security_findings and context.system.public_facing:
        explanations.append(
            ExplanationDraft(
                explanation_type="system_modifier",
                title="Public-facing attack surface",
                description="Open security findings affect a public-facing system, increasing operational exposure.",
                impact_value=-4,
            )
        )
    if active_security_findings and context.system.uses_cjis:
        explanations.append(
            ExplanationDraft(
                explanation_type="system_modifier",
                title="CJIS-sensitive workflow",
                description="Open security findings affect a CJIS-adjacent workflow and require tighter control evidence.",
                impact_value=-5,
            )
        )
    if active_security_findings and context.system.safety_impacting:
        explanations.append(
            ExplanationDraft(
                explanation_type="system_modifier",
                title="Safety-impacting workflow",
                description="Security weaknesses affect a safety-impacting system, increasing review urgency.",
                impact_value=-4,
            )
        )
    if not active_security_findings:
        explanations.append(
            ExplanationDraft(
                explanation_type="remediation_credit",
                title="No active security findings",
                description="No unresolved security, agent-safety, supply-chain, or RAG-integrity findings currently reduce this score.",
                impact_value=2,
            )
        )

    return DomainCalculation(score_domain=domain, score_value=score_from_explanations(domain, explanations), explanations=explanations)
