from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.ai_system import AISystem
from app.models.airb_review import AirbReview
from app.models.assessment import Assessment
from app.models.assessment_profile import AssessmentProfile
from app.models.audit_event import AuditEvent
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.framework_mapping import FrameworkMapping
from app.models.human_appeal_path_check import HumanAppealPathCheck
from app.models.language_access_scenario import LanguageAccessScenario
from app.models.owner import Owner
from app.models.scan_type import ScanType
from app.models.scanner_definition import ScannerDefinition
from app.models.scanner_result import ScannerResult
from app.models.scanner_run import ScannerRun
from app.models.retest import Retest
from app.models.risk_acceptance import RiskAcceptance
from app.models.score import DomainScore, ScoreSnapshot
from app.models.score_explanation import ScoreExplanation
from app.models.score_history import ScoreHistory
from app.seed.phase2_seed import seed_phase2
from app.seed.phase4_seed import seed_phase4
from app.seed.phase6_seed import seed_phase6

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SeedPhase:
    name: str
    run: Callable[[Session], None]
    tables: tuple[tuple[str, type], ...]


@dataclass(frozen=True)
class SeedPhaseResult:
    name: str
    created: dict[str, int]
    skipped_existing: dict[str, int]

    @property
    def created_total(self) -> int:
        return sum(self.created.values())

    @property
    def skipped_total(self) -> int:
        return sum(self.skipped_existing.values())


PHASE2_TABLES = (
    ("owners", Owner),
    ("ai_systems", AISystem),
    ("audit_events", AuditEvent),
)

PHASE4_TABLES = (
    ("scan_types", ScanType),
    ("scanner_definitions", ScannerDefinition),
    ("assessment_profiles", AssessmentProfile),
)

PHASE6_TABLES = (
    ("scan_types", ScanType),
    ("assessment_profiles", AssessmentProfile),
    ("language_access_scenarios", LanguageAccessScenario),
    ("human_appeal_path_checks", HumanAppealPathCheck),
)

SCORE_TABLES = (
    ("domain_scores", DomainScore),
    ("score_explanations", ScoreExplanation),
    ("score_history", ScoreHistory),
    ("score_snapshots", ScoreSnapshot),
    ("audit_events", AuditEvent),
)

SEED_PHASES = (
    SeedPhase("Phase 2 workflow seed data", seed_phase2, PHASE2_TABLES),
    SeedPhase("Phase 4 scanner ecosystem seed data", seed_phase4, PHASE4_TABLES),
    SeedPhase("Phase 6 civil-rights seed data", seed_phase6, PHASE6_TABLES),
)


def seed_database(db: Session) -> list[SeedPhaseResult]:
    logger.info("Starting development bootstrap seed initialization.")
    cleanup = cleanup_seeded_mock_operations(db)
    results = [_run_phase(db, phase) for phase in SEED_PHASES]

    logger.info(
        "Seed initialization complete: created=%s skipped_existing=%s.",
        cleanup.created_total + sum(result.created_total for result in results),
        cleanup.skipped_total + sum(result.skipped_total for result in results),
    )
    return [cleanup, *results]


def cleanup_seeded_mock_operations(db: Session) -> SeedPhaseResult:
    fake_titles = {
        "Prompt injection vulnerability",
        "Spanish-language explanation disparity",
        "Missing human appeal path",
        "Excessive MCP/tool permissions",
        "Incomplete audit logging",
        "Possible sensitive data leakage",
        "Weak governance evidence",
        "Missing bilingual escalation support",
        "Fairness evidence missing for resume triage",
        "Human review evidence incomplete",
        "Accessibility escalation notice gap",
        "Inconsistent policy explanation across languages",
    }
    fake_run_ids = [
        item.id
        for item in db.scalars(
            select(ScannerRun).where(
                (ScannerRun.adapter_name == "mock_adapter")
                | (ScannerRun.scanner_name.like("mock_%"))
                | (ScannerRun.initiated_by == "seed")
            )
        ).all()
    ]
    fake_finding_ids = [
        item.id
        for item in db.scalars(
            select(Finding).where(
                Finding.title.in_(fake_titles)
                | Finding.scanner_name.in_(
                    ["mock-adapter", "civil-rights-manual-review"]
                )
            )
        ).all()
    ]
    fake_assessment_ids = [
        item.id
        for item in db.scalars(
            select(Assessment).where(
                (Assessment.initiated_by == "seed")
                | (
                    Assessment.assessment_type.in_(
                        [
                            "AI assurance baseline",
                            "Security and CJIS workflow review",
                            "Governance readiness review",
                            "RAG integrity review",
                        ]
                    )
                    & Assessment.initiated_by.in_(["Maya Johnson", "Priya Shah", "seed"])
                )
            )
        ).all()
    ]

    deleted: dict[str, int] = {}

    def record(table: str, count: int) -> None:
        if count:
            deleted[table] = count

    if fake_finding_ids:
        record(
            "score_explanations",
            db.query(ScoreExplanation)
            .filter(ScoreExplanation.related_finding_id.in_(fake_finding_ids))
            .delete(synchronize_session=False),
        )
        record(
            "framework_mappings",
            db.query(FrameworkMapping)
            .filter(FrameworkMapping.finding_id.in_(fake_finding_ids))
            .delete(synchronize_session=False),
        )
        record(
            "risk_acceptances",
            db.query(RiskAcceptance)
            .filter(RiskAcceptance.finding_id.in_(fake_finding_ids))
            .delete(synchronize_session=False),
        )
        record(
            "retests",
            db.query(Retest)
            .filter(Retest.finding_id.in_(fake_finding_ids))
            .delete(synchronize_session=False),
        )
        record(
            "evidence",
            db.query(Evidence)
            .filter(Evidence.finding_id.in_(fake_finding_ids))
            .delete(synchronize_session=False),
        )
        record(
            "findings",
            db.query(Finding)
            .filter(Finding.id.in_(fake_finding_ids))
            .delete(synchronize_session=False),
        )

    if fake_run_ids:
        for evidence in db.scalars(select(Evidence)).all():
            if evidence.metadata_json.get("scanner_run_id") in fake_run_ids:
                db.delete(evidence)
                deleted["evidence"] = deleted.get("evidence", 0) + 1
        record(
            "scanner_results",
            db.query(ScannerResult)
            .filter(ScannerResult.scanner_run_id.in_(fake_run_ids))
            .delete(synchronize_session=False),
        )
        record(
            "scanner_runs",
            db.query(ScannerRun)
            .filter(ScannerRun.id.in_(fake_run_ids))
            .delete(synchronize_session=False),
        )

    record(
        "scanner_definitions",
        db.query(ScannerDefinition)
        .filter(
            (ScannerDefinition.adapter_name == "mock_adapter")
            | (ScannerDefinition.scanner_name.like("mock_%"))
        )
        .delete(synchronize_session=False),
    )

    if fake_assessment_ids:
        record(
            "airb_reviews",
            db.query(AirbReview)
            .filter(AirbReview.assessment_id.in_(fake_assessment_ids))
            .delete(synchronize_session=False),
        )
        record(
            "assessments",
            db.query(Assessment)
            .filter(Assessment.id.in_(fake_assessment_ids))
            .delete(synchronize_session=False),
        )

    seed_score_exists = bool(
        db.scalar(select(ScoreHistory.id).where(ScoreHistory.triggered_by == "seed").limit(1))
    )
    if fake_finding_ids or fake_run_ids or fake_assessment_ids or seed_score_exists:
        record("score_explanations", db.query(ScoreExplanation).delete(synchronize_session=False))
        record("domain_scores", db.query(DomainScore).delete(synchronize_session=False))
        record("score_history", db.query(ScoreHistory).delete(synchronize_session=False))
        record("score_snapshots", db.query(ScoreSnapshot).delete(synchronize_session=False))
    db.flush()
    logger.info("Seeded/mock operational cleanup complete: removed=%s.", deleted or {"total": 0})
    return SeedPhaseResult("Seeded/mock operational cleanup", deleted, {})


def _run_phase(db: Session, phase: SeedPhase) -> SeedPhaseResult:
    before = _counts(db, phase.tables)
    logger.info("Running %s.", phase.name)
    phase.run(db)
    db.flush()
    after = _counts(db, phase.tables)

    created = {
        table_name: after[table_name] - before[table_name]
        for table_name, _ in phase.tables
        if after[table_name] - before[table_name] > 0
    }
    skipped_existing = {
        table_name: before[table_name]
        for table_name, _ in phase.tables
        if before[table_name] > 0
    }
    result = SeedPhaseResult(phase.name, created, skipped_existing)
    logger.info(
        "%s complete: created=%s skipped_existing=%s.",
        phase.name,
        created or {"total": 0},
        skipped_existing or {"total": 0},
    )
    return result


def _counts(db: Session, tables: tuple[tuple[str, type], ...]) -> dict[str, int]:
    return {
        table_name: db.scalar(select(func.count()).select_from(model)) or 0
        for table_name, model in tables
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    db = SessionLocal()
    try:
        seed_database(db)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
