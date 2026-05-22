from app.models.enums import AirbReviewStatus, AssessmentStatus, FindingStatus, ScoreDomain
from app.scoring.scoring_rules import (
    DomainCalculation,
    ExplanationDraft,
    ScoringContext,
    active_airb_review,
    calculate_finding_impact,
    finding_explanation,
    matching_findings,
    open_findings,
    score_from_explanations,
)


def calculate(context: ScoringContext) -> DomainCalculation:
    domain = ScoreDomain.governance_evidence.value
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

    active_findings = open_findings(context.findings)
    evidence_by_finding = {item.finding_id for item in context.evidence if item.finding_id}
    missing_evidence_findings = [
        finding for finding in active_findings if finding.id not in evidence_by_finding
    ]
    if not context.evidence:
        explanations.append(
            ExplanationDraft(
                explanation_type="evidence_gap",
                title="No governance evidence uploaded",
                description="No evidence records are linked to this system or assessment.",
                impact_value=-15,
            )
        )
    elif missing_evidence_findings:
        impact = min(18, 4 * len(missing_evidence_findings))
        explanations.append(
            ExplanationDraft(
                explanation_type="evidence_gap",
                title="Open findings missing evidence links",
                description=f"{len(missing_evidence_findings)} open finding(s) do not have direct evidence links.",
                impact_value=-impact,
            )
        )
    else:
        explanations.append(
            ExplanationDraft(
                explanation_type="remediation_credit",
                title="Findings have evidence links",
                description="Active findings have linked evidence records supporting governance review.",
                impact_value=3,
            )
        )

    review = active_airb_review(context)
    if not review:
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title="AIRB workflow missing",
                description="No AI Review Board record is linked to this system or assessment.",
                impact_value=-10,
            )
        )
    elif review.review_status in {
        AirbReviewStatus.pending.value,
        AirbReviewStatus.under_review.value,
    }:
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title="AIRB review incomplete",
                description=f"The current AI Review Board status is {review.review_status.replace('_', ' ')}.",
                impact_value=-6,
            )
        )
    elif review.review_status == AirbReviewStatus.blocked.value:
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title="AIRB review blocked",
                description="The current AI Review Board decision blocks deployment.",
                impact_value=-12,
            )
        )
    elif review.review_status in {
        AirbReviewStatus.approved.value,
        AirbReviewStatus.approved_with_exception.value,
    }:
        explanations.append(
            ExplanationDraft(
                explanation_type="remediation_credit",
                title="AIRB decision recorded",
                description="A governance decision is recorded for this system.",
                impact_value=2,
            )
        )

    if context.assessment and context.assessment.status in {
        AssessmentStatus.draft.value,
        AssessmentStatus.blocked.value,
    }:
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title="Assessment workflow not complete",
                description=f"The assessment status is {context.assessment.status.replace('_', ' ')}, reducing governance readiness.",
                impact_value=-6,
            )
        )
    if not context.audit_events:
        explanations.append(
            ExplanationDraft(
                explanation_type="evidence_gap",
                title="Audit trail missing",
                description="No audit events are linked to this system, assessment, findings, or evidence.",
                impact_value=-8,
            )
        )

    return DomainCalculation(score_domain=domain, score_value=score_from_explanations(domain, explanations), explanations=explanations)
