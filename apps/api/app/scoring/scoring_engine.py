from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models.ai_system import AISystem
from app.models.airb_review import AirbReview
from app.models.assessment import Assessment
from app.models.audit_event import AuditEvent
from app.models.enums import AuditEventType, ScoreDomain
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.score import DomainScore, ScoreSnapshot
from app.models.score_explanation import ScoreExplanation
from app.models.score_history import ScoreHistory
from app.scoring.domain_calculators import (
    bias_civil_rights,
    explainability,
    governance_evidence,
    privacy,
    security,
)
from app.scoring.scoring_rules import (
    CALCULATION_VERSION,
    DOMAIN_WEIGHTS,
    DomainCalculation,
    ExplanationDraft,
    ScoringContext,
    clamp_score,
    domain_label,
    normalize_weights,
    score_band,
)
from app.services.audit_event_service import AuditEventService


class ScoringEngine:
    def __init__(self, db: Session):
        self.db = db
        self.audit = AuditEventService(db)

    def recalculate_system_scores(
        self,
        system_id: str,
        assessment_id: Optional[str] = None,
        *,
        triggered_by: str = "operator",
        change_reason: str = "manual score recalculation",
    ) -> tuple[list[DomainScore], ScoreSnapshot]:
        context = self._build_context(system_id, assessment_id)
        weights = normalize_weights(DOMAIN_WEIGHTS)

        domain_results = [
            security.calculate(context),
            privacy.calculate(context),
            bias_civil_rights.calculate(context),
            explainability.calculate(context),
            governance_evidence.calculate(context),
        ]
        for result in domain_results:
            result.weighted_score = round(result.score_value * weights[result.score_domain], 2)

        overall = self._calculate_overall(domain_results, weights)
        results = [*domain_results, overall]
        scores = [
            self._upsert_score(
                context,
                result,
                triggered_by=triggered_by,
                change_reason=change_reason,
            )
            for result in results
        ]
        snapshot = self._create_snapshot(context, domain_results, overall, weights)
        if context.assessment:
            context.assessment.overall_score = overall.score_value

        self.audit.record(
            entity_type="system",
            entity_id=system_id,
            event_type=AuditEventType.score_recalculated,
            actor=triggered_by,
            new_value=str(overall.score_value),
            notes=change_reason,
        )
        self.db.flush()
        return scores, snapshot

    def recalculate_assessment_scores(
        self,
        assessment_id: str,
        *,
        triggered_by: str = "operator",
        change_reason: str = "manual score recalculation",
    ) -> tuple[list[DomainScore], ScoreSnapshot]:
        assessment = self.db.get(Assessment, assessment_id)
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        return self.recalculate_system_scores(
            assessment.system_id,
            assessment_id,
            triggered_by=triggered_by,
            change_reason=change_reason,
        )

    def _build_context(self, system_id: str, assessment_id: Optional[str]) -> ScoringContext:
        system = self.db.get(AISystem, system_id)
        if not system:
            raise HTTPException(status_code=404, detail="System not found")

        assessment = None
        if assessment_id:
            assessment = self.db.get(Assessment, assessment_id)
            if not assessment:
                raise HTTPException(status_code=404, detail="Assessment not found")
            if assessment.system_id != system_id:
                raise HTTPException(status_code=400, detail="Assessment does not belong to system")
        else:
            assessment = self.db.scalar(
                select(Assessment)
                .where(Assessment.system_id == system_id)
                .order_by(Assessment.created_at.desc())
                .limit(1)
            )

        finding_filters = [Finding.system_id == system_id]
        evidence_filters = [Evidence.system_id == system_id]
        review_filters = [AirbReview.system_id == system_id]
        if assessment_id:
            finding_filters.append(Finding.assessment_id == assessment_id)
            evidence_filters.append(Evidence.assessment_id == assessment_id)
            review_filters.append(AirbReview.assessment_id == assessment_id)

        findings = self.db.scalars(
            select(Finding).where(and_(*finding_filters)).order_by(Finding.created_at)
        ).all()
        evidence = self.db.scalars(
            select(Evidence).where(and_(*evidence_filters)).order_by(Evidence.created_at)
        ).all()
        airb_reviews = self.db.scalars(
            select(AirbReview).where(and_(*review_filters)).order_by(AirbReview.created_at)
        ).all()
        audit_ids = [system_id, *(finding.id for finding in findings), *(item.id for item in evidence)]
        if assessment:
            audit_ids.append(assessment.id)
        audit_events = self.db.scalars(
            select(AuditEvent)
            .where(AuditEvent.entity_id.in_(audit_ids))
            .order_by(AuditEvent.created_at)
        ).all()

        return ScoringContext(
            system=system,
            assessment=assessment,
            findings=list(findings),
            evidence=list(evidence),
            airb_reviews=list(airb_reviews),
            audit_events=list(audit_events),
            today=date.today(),
        )

    def _calculate_overall(
        self,
        domain_results: list[DomainCalculation],
        weights: dict[str, float],
    ) -> DomainCalculation:
        weighted_total = sum(result.score_value * weights[result.score_domain] for result in domain_results)
        overall_score = clamp_score(weighted_total)
        explanations = [
            ExplanationDraft(
                explanation_type="aggregation",
                title=f"{domain_label(result.score_domain)} contribution",
                description=(
                    f"{domain_label(result.score_domain)} Score contributed "
                    f"{round(result.score_value * weights[result.score_domain], 2):g} weighted points "
                    f"using a {round(weights[result.score_domain] * 100):g}% weight."
                ),
                weight=weights[result.score_domain],
                impact_value=round(result.score_value * weights[result.score_domain], 2),
            )
            for result in domain_results
        ]
        explanations.append(
            ExplanationDraft(
                explanation_type="aggregation",
                title=f"Overall risk band: {score_band(overall_score)}",
                description=f"The weighted overall governance score is {overall_score:g}, interpreted as {score_band(overall_score)}.",
                impact_value=0,
            )
        )
        return DomainCalculation(
            score_domain=ScoreDomain.overall_governance.value,
            score_value=overall_score,
            weighted_score=overall_score,
            explanations=explanations,
        )

    def _upsert_score(
        self,
        context: ScoringContext,
        result: DomainCalculation,
        *,
        triggered_by: str,
        change_reason: str,
    ) -> DomainScore:
        score = self.db.scalar(
            select(DomainScore).where(
                DomainScore.system_id == context.system.id,
                DomainScore.assessment_id == (context.assessment.id if context.assessment else None),
                DomainScore.score_domain == result.score_domain,
            )
        )
        previous_score = score.score_value if score else None
        now = datetime.utcnow()
        if not score:
            score = DomainScore(
                system_id=context.system.id,
                assessment_id=context.assessment.id if context.assessment else None,
                score_domain=result.score_domain,
                score_value=result.score_value,
                weighted_score=result.weighted_score,
                calculated_at=now,
                calculation_version=CALCULATION_VERSION,
            )
            self.db.add(score)
            self.db.flush()
        else:
            score.score_value = result.score_value
            score.weighted_score = result.weighted_score
            score.calculated_at = now
            score.calculation_version = CALCULATION_VERSION
            score.explanations.clear()
            self.db.flush()

        for explanation in result.explanations:
            self.db.add(self._to_explanation(score.id, explanation))

        if previous_score is None or abs(previous_score - result.score_value) >= 0.01:
            history = ScoreHistory(
                system_id=context.system.id,
                assessment_id=context.assessment.id if context.assessment else None,
                score_domain=result.score_domain,
                previous_score=previous_score,
                new_score=result.score_value,
                change_reason=change_reason,
                triggered_by=triggered_by,
            )
            self.db.add(history)
            self.audit.record(
                entity_type="score",
                entity_id=score.id,
                event_type=AuditEventType.score_changed,
                actor=triggered_by,
                old_value=None if previous_score is None else str(previous_score),
                new_value=str(result.score_value),
                notes=f"{domain_label(result.score_domain)} score changed: {change_reason}",
            )
        return score

    def _to_explanation(self, score_id: str, draft: ExplanationDraft) -> ScoreExplanation:
        return ScoreExplanation(
            score_id=score_id,
            explanation_type=draft.explanation_type,
            title=draft.title,
            description=draft.description,
            weight=draft.weight,
            impact_value=draft.impact_value,
            related_finding_id=draft.related_finding_id,
        )

    def _create_snapshot(
        self,
        context: ScoringContext,
        domain_results: list[DomainCalculation],
        overall: DomainCalculation,
        weights: dict[str, float],
    ) -> ScoreSnapshot:
        domain_scores = {result.score_domain: result.score_value for result in domain_results}
        sorted_domains = sorted(domain_results, key=lambda result: result.score_value)
        summary = (
            f"Overall governance score is {overall.score_value:g}. "
            f"Lowest domains: {domain_label(sorted_domains[0].score_domain)} {sorted_domains[0].score_value:g}, "
            f"{domain_label(sorted_domains[1].score_domain)} {sorted_domains[1].score_value:g}."
        )
        snapshot = ScoreSnapshot(
            system_id=context.system.id,
            assessment_id=context.assessment.id if context.assessment else None,
            overall_score=overall.score_value,
            domain_scores=domain_scores,
            weights=weights,
            explanation_summary=summary,
            calculation_version=CALCULATION_VERSION,
        )
        self.db.add(snapshot)
        self.db.flush()
        return snapshot
