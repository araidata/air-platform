from app.models.enums import AssessmentStatus, FindingStatus, ScoreDomain
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
    domain = ScoreDomain.explainability.value
    explanations: list[ExplanationDraft] = []

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

    text = evidence_text(context)
    rationale_terms = ["rationale", "explanation", "human review", "review note", "appeal"]
    if not any(term in text for term in rationale_terms):
        explanations.append(
            ExplanationDraft(
                explanation_type="evidence_gap",
                title="Rationale documentation missing",
                description="No rationale, explanation, human-review, or appeal-path evidence is linked to the current record.",
                impact_value=-10,
            )
        )
    if context.assessment and context.assessment.status in {
        AssessmentStatus.draft.value,
        AssessmentStatus.running.value,
        AssessmentStatus.blocked.value,
    }:
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title="Assessment explanation still incomplete",
                description=f"The current assessment is {context.assessment.status.replace('_', ' ')}, so explanation evidence is not yet complete.",
                impact_value=-6,
            )
        )
    open_human_review_findings = [
        finding
        for finding in context.findings
        if any(term in f"{finding.title} {finding.description}".lower() for term in ["human review", "appeal", "rationale"])
        and finding.status not in {FindingStatus.closed.value, FindingStatus.false_positive.value}
    ]
    for finding in open_human_review_findings:
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title=f"Explainability workflow gap: {finding.title}",
                description=f"{finding.title} reduces explainability because review rationale and resident-facing escalation need to be documented.",
                impact_value=-5,
                related_finding_id=finding.id,
            )
        )
    if any(term in text for term in rationale_terms) and not open_human_review_findings:
        explanations.append(
            ExplanationDraft(
                explanation_type="remediation_credit",
                title="Explanation evidence present",
                description="Linked review or rationale evidence supports operator understanding of this system.",
                impact_value=2,
            )
        )

    return DomainCalculation(score_domain=domain, score_value=score_from_explanations(domain, explanations), explanations=explanations)
