from pathlib import Path

from app.core.config import settings
from app.models.assessment_profile import AssessmentProfile
from app.models.enums import ScannerExecutionStatus
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.scan_type import ScanType
from app.models.score import DomainScore
from app.models.scanner_definition import ScannerDefinition
from app.models.scanner_result import ScannerResult
from app.models.scanner_run import ScannerRun
from app.schemas.scanner import ScannerRunCreate
from app.scanners.adapters.base import ScannerExecutionResult
from app.scanners.adapters.mock_adapter import MockScannerAdapter
from app.scanners.normalization.finding_normalizer import normalize_scanner_findings
from app.scanners.services.scanner_execution_service import ScannerExecutionService
from app.tests.factories import create_assessment, create_system


def create_scanner_setup(db):
    system = create_system(db)
    assessment = create_assessment(db, system)
    scanner = ScannerDefinition(
        scanner_name="mock_ai_security_scanner",
        display_name="Mock AI Security Scanner",
        description="Mock security scanner.",
        scanner_category="security",
        adapter_name="mock_adapter",
        scanner_version="0.4.0",
        execution_mode="mock",
        supported_domains=["security", "agent_safety"],
        supported_scan_types=["prompt_injection", "unsafe_tool_use"],
        enabled=True,
        mock_supported=True,
        requires_credentials=False,
    )
    scan_type = ScanType(
        name="prompt_injection",
        display_name="Prompt Injection",
        description="Prompt injection control.",
        domain="security",
        default_severity="high",
        required_for_risk_tiers=["high", "critical"],
        applicable_system_types=["public_facing"],
        evidence_expectations=["raw scanner output", "execution log"],
        enabled=True,
    )
    profile = AssessmentProfile(
        profile_name="Public-Facing Chatbot Review",
        description="Public-facing profile.",
        applicable_risk_tiers=["high"],
        applicable_system_types=["public_facing"],
        required_scan_types=["prompt_injection"],
        optional_scan_types=[],
        required_evidence_types=["raw scanner output"],
        recommended_scanners=["mock_ai_security_scanner"],
        governance_expectations=["Preserve raw evidence."],
        score_domains_affected=["security"],
        enabled=True,
    )
    db.add_all([scanner, scan_type, profile])
    db.flush()
    return system, assessment, scanner, scan_type, profile


def test_mock_adapter_execution_and_normalization_are_deterministic():
    adapter = MockScannerAdapter()
    raw = adapter.execute(
        context=type(
            "Context",
            (),
            {
                "run_id": "run-1",
                "system_id": "system-1",
                "system_name": "Public Benefits Chatbot",
                "risk_tier": "high",
                "scan_type": "prompt_injection",
                "scan_domain": "security",
                "profile_name": "Public-Facing Chatbot Review",
            },
        )()
    )

    parsed = adapter.parse_output(raw.raw_output)
    normalized = normalize_scanner_findings(
        scanner_name="mock_ai_security_scanner",
        scanner_version="0.4.0",
        system_id="system-1",
        assessment_id="assessment-1",
        raw_findings=adapter.normalize_findings(parsed),
        raw_evidence_path="/tmp/raw-output.json",
    )

    assert raw.status == "completed"
    assert normalized[0]["title"] == "Prompt injection vulnerability"
    assert normalized[0]["domain"] == "security"
    assert normalized[0]["evidence"]


def test_scanner_execution_persists_run_artifacts_evidence_findings_and_scores(db_session, tmp_path):
    system, assessment, scanner, scan_type, profile = create_scanner_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            assessment_profile_id=profile.id,
            initiated_by="pytest",
        )
    )
    db_session.flush()

    executed = service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    assert executed.execution_status == ScannerExecutionStatus.completed.value
    assert Path(executed.raw_output_path).exists()
    assert Path(executed.log_path).exists()
    assert db_session.query(ScannerResult).filter_by(scanner_run_id=run.id).one()
    assert db_session.query(Finding).filter_by(system_id=system.id).count() == 1
    run_evidence = [
        item
        for item in db_session.query(Evidence).filter_by(system_id=system.id).all()
        if item.metadata_json.get("scanner_run_id") == run.id
    ]
    assert len(run_evidence) >= 3
    assert db_session.query(DomainScore).filter_by(system_id=system.id).count() >= 6


def test_invalid_scanner_execution_rejects_disabled_scanner(db_session, tmp_path):
    system, assessment, scanner, scan_type, _ = create_scanner_setup(db_session)
    scanner.enabled = False
    service = ScannerExecutionService(db_session, storage_root=tmp_path)

    try:
        service.create_run(
            ScannerRunCreate(
                system_id=system.id,
                assessment_id=assessment.id,
                scanner_definition_id=scanner.id,
                scan_type_id=scan_type.id,
                initiated_by="pytest",
            )
        )
    except Exception as exc:
        assert getattr(exc, "status_code", None) == 400
    else:
        raise AssertionError("Disabled scanner should not create a run")


def test_malformed_scanner_output_fails_run_and_preserves_failure_log(db_session, tmp_path):
    system, assessment, scanner, scan_type, _ = create_scanner_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            initiated_by="pytest",
        )
    )

    class MalformedAdapter:
        def execute(self, context):
            return ScannerExecutionResult(
                status="completed",
                raw_output={"scanner": "bad", "findings": "not-a-list"},
                logs="malformed output",
            )

        def parse_output(self, raw_output):
            raise ValueError("malformed scanner output")

        def normalize_findings(self, parsed_output):
            return []

    service._adapter_for = lambda adapter_name: MalformedAdapter()
    executed = service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    assert executed.execution_status == ScannerExecutionStatus.failed.value
    assert "malformed scanner output" in executed.error_message
    assert Path(executed.raw_output_path).exists()
    assert Path(executed.log_path).exists()
    assert db_session.query(Finding).filter_by(system_id=system.id).count() == 0


def test_scanner_api_routes_create_execute_and_recommend(client, tmp_path):
    settings.scanner_storage_root = str(tmp_path)
    system = client.post(
        "/systems",
        json={
            "system_name": "Public Benefits Chatbot",
            "department_owner": "Health and Human Services",
            "business_purpose": "Answers public benefits questions.",
            "public_facing": True,
            "rights_impacting": True,
            "uses_pii": True,
            "deployment_environment": "pilot",
            "risk_tier": "high",
            "approval_status": "under_review",
        },
    ).json()
    assessment = client.post(
        "/assessments",
        json={
            "system_id": system["id"],
            "assessment_type": "AI assurance baseline",
            "initiated_by": "Maya Johnson",
        },
    ).json()
    scanner = client.post(
        "/scanner-definitions",
        json={
            "scanner_name": "mock_ai_security_scanner",
            "display_name": "Mock AI Security Scanner",
            "description": "Mock security scanner.",
            "scanner_category": "security",
            "adapter_name": "mock_adapter",
            "scanner_version": "0.4.0",
            "execution_mode": "mock",
            "supported_domains": ["security"],
            "supported_scan_types": ["prompt_injection"],
            "enabled": True,
            "mock_supported": True,
            "requires_credentials": False,
        },
    ).json()
    scan_type = client.post(
        "/scan-types",
        json={
            "name": "prompt_injection",
            "display_name": "Prompt Injection",
            "description": "Prompt injection control.",
            "domain": "security",
            "default_severity": "high",
            "required_for_risk_tiers": ["high"],
            "applicable_system_types": ["public_facing"],
            "evidence_expectations": ["raw scanner output"],
            "enabled": True,
        },
    ).json()
    profile = client.post(
        "/assessment-profiles",
        json={
            "profile_name": "Public-Facing Chatbot Review",
            "description": "Public profile.",
            "applicable_risk_tiers": ["high"],
            "applicable_system_types": ["public_facing"],
            "required_scan_types": ["prompt_injection"],
            "optional_scan_types": [],
            "required_evidence_types": ["raw scanner output"],
            "recommended_scanners": ["mock_ai_security_scanner"],
            "governance_expectations": ["Preserve raw output."],
            "score_domains_affected": ["security"],
            "enabled": True,
        },
    ).json()

    recommendations = client.get(
        f"/systems/{system['id']}/recommended-scans?assessment_profile_id={profile['id']}"
    )
    assert recommendations.status_code == 200
    assert recommendations.json()["required_scans"]

    run = client.post(
        "/scanner-runs",
        json={
            "system_id": system["id"],
            "assessment_id": assessment["id"],
            "scanner_definition_id": scanner["id"],
            "scan_type_id": scan_type["id"],
            "assessment_profile_id": profile["id"],
            "initiated_by": "pytest",
        },
    )
    assert run.status_code == 201

    executed = client.post(
        f"/scanner-runs/{run.json()['id']}/execute",
        json={"initiated_by": "pytest"},
    )
    assert executed.status_code == 200
    assert executed.json()["execution_status"] == "completed"
    assert client.get(f"/systems/{system['id']}/scanner-runs").json()
    assert client.get("/scanner-adapters").json()[0]["adapter_name"] == "mock_adapter"
