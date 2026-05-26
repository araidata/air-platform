from sqlalchemy import func, select

from app.core.config import settings
from app.models.ai_system import AISystem
from app.models.airb_review import AirbReview
from app.models.assessment import Assessment
from app.models.assessment_profile import AssessmentProfile
from app.models.audit_event import AuditEvent
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.human_appeal_path_check import HumanAppealPathCheck
from app.models.language_access_scenario import LanguageAccessScenario
from app.models.scan_type import ScanType
from app.models.scanner_definition import ScannerDefinition
from app.models.scanner_result import ScannerResult
from app.models.scanner_run import ScannerRun
from app.models.score import DomainScore, ScoreSnapshot
from app.models.score_explanation import ScoreExplanation
from app.models.score_history import ScoreHistory
from app.seed.run_seed import seed_database


COUNTED_MODELS = (
    AISystem,
    Assessment,
    Finding,
    Evidence,
    AuditEvent,
    AirbReview,
    ScannerDefinition,
    ScanType,
    AssessmentProfile,
    ScannerRun,
    ScannerResult,
    LanguageAccessScenario,
    HumanAppealPathCheck,
    DomainScore,
    ScoreExplanation,
    ScoreHistory,
    ScoreSnapshot,
)


def _counts(db):
    return {
        model.__tablename__: db.scalar(select(func.count()).select_from(model)) or 0
        for model in COUNTED_MODELS
    }


def test_development_seed_bootstrap_runs_all_phases_and_is_idempotent(
    db_session, tmp_path, monkeypatch
):
    monkeypatch.setattr(settings, "scanner_storage_root", str(tmp_path))

    first_results = seed_database(db_session)
    db_session.commit()
    first_counts = _counts(db_session)

    assert [result.name for result in first_results][:4] == [
        "Seeded/mock operational cleanup",
        "Phase 2 workflow seed data",
        "Phase 4 scanner ecosystem seed data",
        "Phase 6 civil-rights seed data",
    ]
    assert first_counts["ai_systems"] == 5
    assert first_counts["scanner_definitions"] >= 11
    assert first_counts["scan_types"] >= 35
    assert first_counts["assessment_profiles"] >= 7
    assert first_counts["scanner_runs"] == 0
    assert first_counts["scanner_results"] == 0
    assert first_counts["language_access_scenarios"] >= 3
    assert first_counts["human_appeal_path_checks"] >= 4
    assert first_counts["findings"] == 0
    assert first_counts["evidence"] == 0
    assert first_counts["domain_scores"] == 0
    assert first_counts["score_history"] == 0

    second_results = seed_database(db_session)
    db_session.commit()
    second_counts = _counts(db_session)

    assert second_counts == first_counts
    assert all(result.created_total == 0 for result in second_results)
    assert sum(result.skipped_total for result in second_results) > 0
