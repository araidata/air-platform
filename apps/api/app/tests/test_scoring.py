import pytest

from app.models.enums import ScoreDomain
from app.models.finding import Finding
from app.models.score import DomainScore
from app.models.score_explanation import ScoreExplanation
from app.models.score_history import ScoreHistory
from app.schemas.finding import FindingCreate, FindingUpdate
from app.scoring.scoring_engine import ScoringEngine
from app.scoring.scoring_rules import DOMAIN_WEIGHTS, clamp_score, normalize_weights
from app.services.finding_workflow_service import FindingWorkflowService
from app.tests.factories import create_assessment, create_owner, create_system
from app.tests.test_api_routes import create_api_finding


def create_scored_finding(db, *, severity="critical", domain="security") -> Finding:
    owner = create_owner(db)
    system = create_system(db)
    assessment = create_assessment(db, system)
    return FindingWorkflowService(db).create(
        FindingCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_name="mock-adapter",
            scanner_version="0.1.0",
            domain=domain,
            severity=severity,
            confidence="high",
            title="Prompt injection vulnerability",
            description="Unsafe instruction override was observed.",
            evidence_summary="Prompt and response demonstrate override behavior.",
            remediation="Add prompt injection tests and tool gating.",
            owner_id=owner.id,
            approval_blocking=True,
            actor="Maya Johnson",
        )
    )


def test_score_calculation_generates_explanations_history_and_overall(db_session):
    finding = create_scored_finding(db_session)
    db_session.commit()

    scores = db_session.query(DomainScore).filter_by(system_id=finding.system_id).all()
    by_domain = {score.score_domain: score for score in scores}

    assert by_domain[ScoreDomain.security.value].score_value < 100
    assert by_domain[ScoreDomain.overall_governance.value].score_value < 100
    assert (
        db_session.query(ScoreExplanation)
        .filter_by(score_id=by_domain[ScoreDomain.security.value].id)
        .count()
        >= 1
    )
    assert db_session.query(ScoreHistory).filter_by(system_id=finding.system_id).count() >= 6


def test_weighted_aggregation_matches_domain_weights(db_session):
    finding = create_scored_finding(db_session, severity="high")
    scores, _ = ScoringEngine(db_session).recalculate_system_scores(
        finding.system_id,
        finding.assessment_id,
        triggered_by="test",
        change_reason="test aggregation",
    )
    by_domain = {score.score_domain: score.score_value for score in scores}
    expected = round(
        sum(by_domain[domain] * weight for domain, weight in DOMAIN_WEIGHTS.items()),
        2,
    )

    assert by_domain[ScoreDomain.overall_governance.value] == expected


def test_closed_findings_stop_affecting_domain_score(db_session):
    finding = create_scored_finding(db_session, severity="critical")
    first_security_score = db_session.query(DomainScore).filter_by(
        system_id=finding.system_id,
        assessment_id=finding.assessment_id,
        score_domain=ScoreDomain.security.value,
    ).one().score_value

    finding.status = "closed"
    ScoringEngine(db_session).recalculate_system_scores(
        finding.system_id,
        finding.assessment_id,
        triggered_by="test",
        change_reason="finding closed",
    )
    updated_security_score = db_session.query(DomainScore).filter_by(
        system_id=finding.system_id,
        assessment_id=finding.assessment_id,
        score_domain=ScoreDomain.security.value,
    ).one()

    assert updated_security_score.score_value > first_security_score


def test_score_history_records_score_changes_from_finding_updates(db_session):
    finding = create_scored_finding(db_session, severity="medium")
    initial_history_count = db_session.query(ScoreHistory).filter_by(
        system_id=finding.system_id,
        score_domain=ScoreDomain.security.value,
    ).count()

    FindingWorkflowService(db_session).update(
        finding,
        FindingUpdate(severity="critical", actor="Maya Johnson", notes="Severity raised."),
    )
    db_session.commit()

    assert (
        db_session.query(ScoreHistory)
        .filter_by(system_id=finding.system_id, score_domain=ScoreDomain.security.value)
        .count()
        > initial_history_count
    )


def test_score_bounds_and_weight_normalization_are_guarded():
    assert clamp_score(-25) == 0
    assert clamp_score(125) == 100
    assert normalize_weights({"a": 2, "b": 2}) == {"a": 0.5, "b": 0.5}
    with pytest.raises(ValueError):
        normalize_weights({"a": 0})


def test_score_api_routes_recalculate_and_expose_explanations(client):
    system, assessment, _ = create_api_finding(client)

    scores_response = client.get(f"/systems/{system['id']}/scores")
    assert scores_response.status_code == 200
    scores = scores_response.json()
    assert {score["score_domain"] for score in scores} >= {
        "security",
        "privacy",
        "bias_civil_rights",
        "explainability",
        "governance_evidence",
        "overall_governance",
    }

    security_score = next(score for score in scores if score["score_domain"] == "security")
    explanations = client.get(f"/scores/{security_score['id']}/explanations")
    assert explanations.status_code == 200
    assert explanations.json()

    recalc = client.post(
        f"/assessments/{assessment['id']}/recalculate-scores",
        json={"triggered_by": "pytest", "change_reason": "API scoring test"},
    )
    assert recalc.status_code == 200
    assert recalc.json()["snapshot"]["overall_score"] >= 0

    history = client.get(f"/systems/{system['id']}/score-history")
    assert history.status_code == 200
    assert history.json()
