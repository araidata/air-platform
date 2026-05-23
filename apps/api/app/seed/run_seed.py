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
from app.models.score import DomainScore, ScoreSnapshot
from app.models.score_explanation import ScoreExplanation
from app.models.score_history import ScoreHistory
from app.seed.phase2_seed import recalculate_seed_scores, seed_phase2
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
    ("assessments", Assessment),
    ("findings", Finding),
    ("evidence", Evidence),
    ("framework_mappings", FrameworkMapping),
    ("airb_reviews", AirbReview),
    ("audit_events", AuditEvent),
)

PHASE4_TABLES = (
    ("scan_types", ScanType),
    ("scanner_definitions", ScannerDefinition),
    ("assessment_profiles", AssessmentProfile),
    ("scanner_runs", ScannerRun),
    ("scanner_results", ScannerResult),
    ("findings", Finding),
    ("evidence", Evidence),
    ("audit_events", AuditEvent),
    ("domain_scores", DomainScore),
    ("score_history", ScoreHistory),
)

PHASE6_TABLES = (
    ("scan_types", ScanType),
    ("assessment_profiles", AssessmentProfile),
    ("language_access_scenarios", LanguageAccessScenario),
    ("human_appeal_path_checks", HumanAppealPathCheck),
    ("findings", Finding),
    ("evidence", Evidence),
    ("airb_reviews", AirbReview),
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
    logger.info("Starting development/demo bootstrap seed initialization.")
    results = [_run_phase(db, phase) for phase in SEED_PHASES]

    if _should_recalculate_scores(db, results):
        results.append(
            _run_phase(
                db,
                SeedPhase("Phase 3 score recalculation", recalculate_seed_scores, SCORE_TABLES),
            )
        )
    else:
        logger.info("Skipping Phase 3 score recalculation; seeded scores are already present.")

    logger.info(
        "Seed initialization complete: created=%s skipped_existing=%s.",
        sum(result.created_total for result in results),
        sum(result.skipped_total for result in results),
    )
    return results


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


def _should_recalculate_scores(db: Session, results: list[SeedPhaseResult]) -> bool:
    if any(result.created_total for result in results):
        return True
    system_count = db.scalar(select(func.count()).select_from(AISystem)) or 0
    score_count = db.scalar(select(func.count()).select_from(DomainScore)) or 0
    return system_count > 0 and score_count < system_count * 6


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
