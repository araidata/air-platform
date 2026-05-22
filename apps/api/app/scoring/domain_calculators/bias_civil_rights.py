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
    domain = ScoreDomain.bias_civil_rights.value
    explanations: list[ExplanationDraft] = []

    active_bias_findings = []
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
                active_bias_findings.append(finding)

    open_appeal_findings = [
        finding
        for finding in context.findings
        if any(
            term in f"{finding.title} {finding.description}".lower()
            for term in ["appeal", "human review", "escalation"]
        )
        and finding.status not in {FindingStatus.closed.value, FindingStatus.false_positive.value}
    ]
    if open_appeal_findings:
        for finding in open_appeal_findings:
            explanations.append(
                ExplanationDraft(
                    explanation_type="workflow_gap",
                    title="Human appeal path gap",
                    description=f"{finding.title} reduced the Bias & Civil Rights Score because rights-impacting workflows need clear human appeal paths.",
                    impact_value=-12,
                    related_finding_id=finding.id,
                )
            )
    elif context.system.rights_impacting and "appeal" not in evidence_text(context):
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title="Appeal-path evidence missing",
                description="The system is rights-impacting, but no human appeal path evidence is linked.",
                impact_value=-8,
            )
        )

    if context.system.rights_impacting and not active_bias_findings and not open_appeal_findings:
        explanations.append(
            ExplanationDraft(
                explanation_type="system_modifier",
                title="Rights-impacting workflow",
                description="Rights-impacting systems require ongoing civil-rights evidence even when no active bias finding is open.",
                impact_value=-3,
            )
        )
    if any("language" in f"{finding.title} {finding.description}".lower() for finding in active_bias_findings):
        explanations.append(
            ExplanationDraft(
                explanation_type="workflow_gap",
                title="Language access concern",
                description="An unresolved language-access finding affects public-service equity and review readiness.",
                impact_value=-4,
            )
        )
    linked_evidence = evidence_text(context)
    if context.system.public_facing and "language" not in linked_evidence:
        explanations.append(
            ExplanationDraft(
                explanation_type="evidence_gap",
                title="Language-access evidence missing",
                description="Public-facing systems need bilingual scenario evidence or translated response evidence.",
                impact_value=-5,
            )
        )
    if context.system.public_facing and "accessibility" not in linked_evidence:
        explanations.append(
            ExplanationDraft(
                explanation_type="evidence_gap",
                title="Accessibility evidence missing",
                description="Public-facing systems need accessibility notices, escalation paths, or accommodation evidence.",
                impact_value=-4,
            )
        )

    latest_review = sorted(context.airb_reviews, key=lambda review: review.updated_at, reverse=True)[0] if context.airb_reviews else None
    if latest_review and context.system.rights_impacting:
        if latest_review.civil_rights_review_status in {"not_started", "needs_evidence"}:
            explanations.append(
                ExplanationDraft(
                    explanation_type="workflow_gap",
                    title="Civil-rights AIRB review incomplete",
                    description="AIRB civil-rights review status is not complete for a rights-impacting system.",
                    impact_value=-6,
                )
            )
        if not latest_review.appeal_path_validated:
            explanations.append(
                ExplanationDraft(
                    explanation_type="workflow_gap",
                    title="AIRB appeal-path validation missing",
                    description="The AIRB record does not show appeal-path validation for the rights-impacting workflow.",
                    impact_value=-5,
                )
            )

    return DomainCalculation(score_domain=domain, score_value=score_from_explanations(domain, explanations), explanations=explanations)
