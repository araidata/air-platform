import pytest
from fastapi import HTTPException

from app.models.audit_event import AuditEvent
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.schemas.evidence import EvidenceCreate
from app.schemas.finding import FindingCreate, FindingTransition
from app.schemas.retest import RetestCreate, RetestUpdate
from app.services.evidence_service import EvidenceService
from app.services.finding_workflow_service import FindingWorkflowService
from app.services.retest_service import RetestService
from app.tests.factories import create_assessment, create_owner, create_system


def finding_payload(system, assessment, owner):
    return FindingCreate(
        system_id=system.id,
        assessment_id=assessment.id,
        scanner_name="manual-review",
        scanner_version="0.1.0",
        domain="security",
        severity="high",
        confidence="medium",
        title="Prompt injection vulnerability",
        description="Unsafe instruction override was observed.",
        evidence_summary="Prompt and response demonstrate override behavior.",
        remediation="Add prompt injection tests and tool gating.",
        owner_id=owner.id,
        score_impact={"security": -8},
        actor="Maya Johnson",
    )


def test_model_creation(db_session):
    owner = create_owner(db_session)
    system = create_system(db_session)
    assessment = create_assessment(db_session, system)
    finding = FindingWorkflowService(db_session).create(
        finding_payload(system, assessment, owner)
    )
    db_session.commit()

    assert db_session.get(Finding, finding.id).title == "Prompt injection vulnerability"
    assert db_session.query(AuditEvent).filter_by(event_type="finding_created").count() == 1


def test_valid_finding_status_transition_creates_audit_event(db_session):
    owner = create_owner(db_session)
    system = create_system(db_session)
    assessment = create_assessment(db_session, system)
    finding = FindingWorkflowService(db_session).create(
        finding_payload(system, assessment, owner)
    )

    FindingWorkflowService(db_session).transition(
        finding,
        FindingTransition(
            status="under_review",
            actor="Maya Johnson",
            notes="Triage started.",
        ),
    )
    db_session.commit()

    assert finding.status == "under_review"
    assert (
        db_session.query(AuditEvent)
        .filter_by(event_type="finding_status_changed", entity_id=finding.id)
        .count()
        == 1
    )


def test_invalid_finding_status_transition_is_rejected(db_session):
    owner = create_owner(db_session)
    system = create_system(db_session)
    assessment = create_assessment(db_session, system)
    finding = FindingWorkflowService(db_session).create(
        finding_payload(system, assessment, owner)
    )

    with pytest.raises(HTTPException):
        FindingWorkflowService(db_session).transition(
            finding,
            FindingTransition(status="closed", actor="Maya Johnson"),
        )


def test_evidence_creation_links_and_audits(db_session):
    owner = create_owner(db_session)
    system = create_system(db_session)
    assessment = create_assessment(db_session, system)
    finding = FindingWorkflowService(db_session).create(
        finding_payload(system, assessment, owner)
    )

    evidence = EvidenceService(db_session).create(
        EvidenceCreate(
            finding_id=finding.id,
            evidence_type="prompt",
            title="Prompt evidence",
            raw_text="Ignore previous instructions.",
            content_type="text/plain",
            created_by="Maya Johnson",
        )
    )
    db_session.commit()

    assert db_session.get(Evidence, evidence.id).assessment_id == assessment.id
    assert db_session.query(AuditEvent).filter_by(event_type="evidence_created").count() == 1


def test_retest_creation_and_update_audits(db_session):
    owner = create_owner(db_session)
    system = create_system(db_session)
    assessment = create_assessment(db_session, system)
    finding = FindingWorkflowService(db_session).create(
        finding_payload(system, assessment, owner)
    )

    retest = RetestService(db_session).create(
        finding.id,
        RetestCreate(initiated_by="Maya Johnson", notes="Validate remediation."),
    )
    RetestService(db_session).update(
        retest,
        RetestUpdate(
            status="passed",
            result_summary="Prompt injection no longer reproduced.",
            actor="Maya Johnson",
        ),
    )
    db_session.commit()

    assert retest.status == "passed"
    assert finding.retest_status == "passed"
    assert db_session.query(AuditEvent).filter_by(event_type="retest_created").count() == 1
    assert (
        db_session.query(AuditEvent)
        .filter_by(event_type="retest_status_changed")
        .count()
        >= 2
    )
