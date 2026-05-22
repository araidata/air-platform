from app.models.assessment_profile import AssessmentProfile
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.human_appeal_path_check import HumanAppealPathCheck
from app.models.language_access_scenario import LanguageAccessScenario
from app.models.score import DomainScore
from app.scoring.scoring_engine import ScoringEngine
from app.seed.phase6_seed import seed_phase6
from app.services.evidence_service import EvidenceService
from app.schemas.evidence import EvidenceCreate
from app.tests.factories import create_assessment, create_system


def test_phase6_seed_adds_templates_scenarios_findings_and_airb_indicators(db_session):
    system = create_system(db_session)
    assessment = create_assessment(db_session, system)
    db_session.flush()

    seed_phase6(db_session)
    ScoringEngine(db_session).recalculate_system_scores(
        system.id,
        assessment.id,
        triggered_by="pytest",
        change_reason="phase 6 seed test",
    )
    db_session.commit()

    template_names = {
        profile.profile_name for profile in db_session.query(AssessmentProfile).all()
    }
    assert "Rights-Impacting AI Review" in template_names
    assert "Accessibility and Language Access Review" in template_names
    assert db_session.query(LanguageAccessScenario).count() >= 1
    assert db_session.query(HumanAppealPathCheck).count() >= 1
    assert db_session.query(Finding).filter_by(domain="bias_civil_rights").count() >= 1
    assert db_session.query(Evidence).filter(
        Evidence.evidence_type.in_(["translated_response", "accessibility_evidence"])
    ).count() >= 1
    assert db_session.query(DomainScore).filter_by(system_id=system.id).count() >= 6


def test_language_access_scenario_api_rejects_unsupported_language_pair(client):
    system = client.post(
        "/systems",
        json={
            "system_name": "Language Test System",
            "department_owner": "County Manager",
            "business_purpose": "Tests language access.",
            "public_facing": True,
            "rights_impacting": True,
            "deployment_environment": "pilot",
            "risk_tier": "high",
        },
    ).json()
    response = client.post(
        "/civil-rights/language-access-scenarios",
        json={
            "system_id": system["id"],
            "name": "Unsupported language scenario",
            "primary_language": "English",
            "comparison_language": "Klingon",
            "scenario_type": "policy_explanation",
            "prompt_text": "Explain appeal rights.",
            "expected_behavior": "Equivalent explanation.",
            "evidence_requirements": ["transcript"],
        },
    )

    assert response.status_code == 422


def test_validated_appeal_path_check_requires_evidence(client):
    system = client.post(
        "/systems",
        json={
            "system_name": "Appeal Test System",
            "department_owner": "Human Resources",
            "business_purpose": "Tests appeal checks.",
            "rights_impacting": True,
            "uses_pii": True,
            "deployment_environment": "pilot",
            "risk_tier": "high",
        },
    ).json()

    response = client.post(
        "/civil-rights/appeal-path-checks",
        json={
            "system_id": system["id"],
            "check_type": "candidate_appeal",
            "status": "validated",
            "required_control": "Candidate appeal process exists.",
            "evidence_requirements": ["appeal policy"],
            "evidence_ids": [],
        },
    )

    assert response.status_code == 422


def test_invalid_fairness_finding_domain_is_rejected(client):
    system = client.post(
        "/systems",
        json={
            "system_name": "Fairness Finding Test System",
            "department_owner": "Civil Rights Office",
            "business_purpose": "Tests fairness finding validation.",
            "rights_impacting": True,
            "deployment_environment": "pilot",
            "risk_tier": "high",
        },
    ).json()
    assessment = client.post(
        "/assessments",
        json={
            "system_id": system["id"],
            "assessment_type": "Rights-Impacting AI Review",
            "initiated_by": "Luis Ramirez",
        },
    ).json()

    response = client.post(
        "/findings",
        json={
            "system_id": system["id"],
            "assessment_id": assessment["id"],
            "scanner_name": "civil-rights-manual-review",
            "scanner_version": "phase6",
            "domain": "protected_class_disparity",
            "severity": "high",
            "confidence": "medium",
            "title": "Unsupported fairness finding shape",
            "description": "Category was incorrectly submitted as a domain.",
            "evidence_summary": "Malformed fairness finding.",
            "remediation": "Use domain bias_civil_rights and preserve the category in evidence metadata.",
            "actor": "Luis Ramirez",
        },
    )

    assert response.status_code == 422


def test_fairness_evidence_relationship_and_score_recalculation(db_session):
    system = create_system(db_session)
    assessment = create_assessment(db_session, system)
    finding = Finding(
        system_id=system.id,
        assessment_id=assessment.id,
        scanner_name="manual-review",
        scanner_version="phase6",
        domain="bias_civil_rights",
        severity="high",
        confidence="high",
        title="Appeal path missing",
        description="Human appeal path is missing.",
        evidence_summary="No appeal process evidence is linked.",
        remediation="Document appeal path and bilingual escalation.",
        score_impact={"bias_civil_rights": -8},
        approval_blocking=True,
    )
    db_session.add(finding)
    db_session.flush()

    evidence = EvidenceService(db_session).create(
        EvidenceCreate(
            finding_id=finding.id,
            evidence_type="appeal_process_documentation",
            title="Appeal procedure",
            raw_text="Residents may request human review through the benefits office.",
            created_by="Luis Ramirez",
            metadata_json={"phase": "6"},
        )
    )
    db_session.commit()

    assert evidence.finding_id == finding.id
    assert evidence.assessment_id == assessment.id
    assert evidence.system_id == system.id
    assert db_session.query(DomainScore).filter_by(
        system_id=system.id,
        assessment_id=assessment.id,
        score_domain="bias_civil_rights",
    ).one().score_value < 100


def test_civil_rights_summary_api_returns_phase6_records(client):
    system = client.post(
        "/systems",
        json={
            "system_name": "Public Benefits Chatbot",
            "department_owner": "Health and Human Services",
            "business_purpose": "Answers benefits questions.",
            "public_facing": True,
            "rights_impacting": True,
            "uses_pii": True,
            "deployment_environment": "pilot",
            "risk_tier": "high",
        },
    ).json()
    assessment = client.post(
        "/assessments",
        json={
            "system_id": system["id"],
            "assessment_type": "Public Benefits Eligibility AI Review",
            "initiated_by": "Maya Johnson",
        },
    ).json()
    scenario = client.post(
        "/civil-rights/language-access-scenarios",
        json={
            "system_id": system["id"],
            "assessment_id": assessment["id"],
            "name": "Benefits appeal bilingual test",
            "primary_language": "English",
            "comparison_language": "Spanish",
            "scenario_type": "appeal_path",
            "prompt_text": "How do I appeal a benefits decision?",
            "expected_behavior": "Equivalent appeal instructions.",
            "evidence_requirements": ["English transcript", "Spanish transcript"],
        },
    )
    assert scenario.status_code == 201

    summary = client.get("/civil-rights/summary")
    assert summary.status_code == 200
    assert summary.json()["language_access_scenarios"][0]["name"] == "Benefits appeal bilingual test"
