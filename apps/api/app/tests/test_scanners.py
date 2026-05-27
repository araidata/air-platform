from pathlib import Path
import subprocess

from app.core.config import settings
from app.models.assessment_profile import AssessmentProfile
from app.models.enums import ScannerExecutionStatus
from app.models.evidence import Evidence
from app.models.finding import Finding
from app.models.framework_mapping import FrameworkMapping
from app.models.scan_type import ScanType
from app.models.score import DomainScore
from app.models.scanner_definition import ScannerDefinition
from app.models.scanner_result import ScannerResult
from app.models.scanner_run import ScannerRun
from app.schemas.scanner import ScannerRunCreate
from app.scanners.adapters.base import ScannerExecutionResult
from app.scanners.adapters.garak_adapter import GarakCliAdapter
from app.scanners.adapters.giskard_adapter import GiskardAdapter
from app.scanners.adapters.pyrit_adapter import PyRITAdapter
from app.scanners.services.scanner_execution_service import ScannerExecutionService
from app.services.opencontrol_service import OpenControlService
from app.tests.factories import create_assessment, create_system


def create_scanner_setup(db):
    system = create_system(db)
    assessment = create_assessment(db, system)
    scanner = ScannerDefinition(
        scanner_name="agentseal",
        display_name="AgentSeal",
        description="Future CLI scanner without executable adapter in this runtime.",
        scanner_category="security",
        adapter_name="agentseal_cli_adapter",
        scanner_version="future",
        execution_mode="cli",
        supported_domains=["security", "agent_safety"],
        supported_scan_types=["prompt_injection", "unsafe_tool_use"],
        enabled=True,
        mock_supported=False,
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
        recommended_scanners=["agentseal"],
        governance_expectations=["Preserve raw evidence."],
        score_domains_affected=["security"],
        enabled=True,
    )
    db.add_all([scanner, scan_type, profile])
    db.flush()
    return system, assessment, scanner, scan_type, profile


def create_garak_setup(db):
    system = create_system(db)
    assessment = create_assessment(db, system)
    scanner = ScannerDefinition(
        scanner_name="garak",
        display_name="garak",
        description="Real garak CLI scanner.",
        scanner_category="security",
        adapter_name="garak_cli_adapter",
        scanner_version="0.15.x",
        execution_mode="cli",
        supported_domains=["security"],
        supported_scan_types=["prompt_injection"],
        enabled=True,
        mock_supported=False,
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
        evidence_expectations=["native garak JSONL report", "execution log"],
        enabled=True,
    )
    db.add_all([scanner, scan_type])
    db.flush()
    return system, assessment, scanner, scan_type


def create_giskard_setup(db):
    system = create_system(db)
    assessment = create_assessment(db, system)
    system.scanner_compatible = ["giskard", "prompt_injection"]
    scanner = ScannerDefinition(
        scanner_name="giskard",
        display_name="Giskard",
        description="Real Giskard scanner.",
        scanner_category="ai_quality",
        adapter_name="giskard_adapter",
        scanner_version="2.x",
        execution_mode="python",
        supported_domains=["security", "explainability", "bias_civil_rights", "rag_integrity"],
        supported_scan_types=["prompt_injection", "hallucination"],
        enabled=True,
        mock_supported=False,
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
        evidence_expectations=["Giskard report", "prompt response records"],
        enabled=True,
    )
    db.add_all([scanner, scan_type])
    db.flush()
    return system, assessment, scanner, scan_type


def create_pyrit_setup(db):
    system = create_system(db)
    assessment = create_assessment(db, system)
    system.scanner_compatible = ["pyrit", "data_exfiltration"]
    scanner = ScannerDefinition(
        scanner_name="pyrit",
        display_name="PyRIT",
        description="Real PyRIT scanner.",
        scanner_category="security",
        adapter_name="pyrit_adapter",
        scanner_version="0.13.x",
        execution_mode="python",
        supported_domains=["security"],
        supported_scan_types=["data_exfiltration"],
        enabled=True,
        mock_supported=False,
        requires_credentials=False,
    )
    scan_type = ScanType(
        name="data_exfiltration",
        display_name="Data Exfiltration",
        description="Data exfiltration control.",
        domain="security",
        default_severity="critical",
        required_for_risk_tiers=["high", "critical"],
        applicable_system_types=["public_facing"],
        evidence_expectations=["attack prompts", "target responses"],
        enabled=True,
    )
    db.add_all([scanner, scan_type])
    db.flush()
    return system, assessment, scanner, scan_type


def test_no_mock_adapter_is_registered(client):
    adapters = client.get("/scanner-adapters").json()

    assert [adapter["adapter_name"] for adapter in adapters] == [
        "garak_cli_adapter",
        "giskard_adapter",
        "pyrit_adapter",
    ]
    assert all(adapter["mock_supported"] is False for adapter in adapters)


def test_garak_adapter_parses_and_normalizes_report_records(tmp_path):
    adapter = GarakCliAdapter()
    parsed = adapter.parse_output(
        {
            "scan_type": "prompt_injection",
            "scan_domain": "security",
            "report_records": [
                {
                    "entry_type": "eval",
                    "probe": "promptinject.Test",
                    "detector": "always.Fail",
                    "passed": 2,
                    "total": 10,
                }
            ],
        }
    )

    findings = adapter.normalize_findings(parsed)

    assert findings[0]["title"] == "garak detected prompt injection risk"
    assert findings[0]["severity"] == "critical"
    assert findings[0]["score_impact"]["security"] == -14
    assert findings[0]["evidence"][0]["content_type"] == "application/json"


def test_garak_adapter_handles_empty_report_without_findings():
    adapter = GarakCliAdapter()
    parsed = adapter.parse_output({"report_records": [], "scan_type": "prompt_injection"})

    assert adapter.normalize_findings(parsed) == []


def test_garak_adapter_handles_partial_eval_records():
    adapter = GarakCliAdapter()
    parsed = adapter.parse_output(
        {
            "scan_type": "prompt_injection",
            "scan_domain": "security",
            "report_records": [
                {
                    "entry_type": "eval",
                    "probe": "promptinject.HijackLongPrompt",
                    "detector": "promptinject.AttackRogueString",
                    "fails": 1,
                    "total_evaluated": 4,
                }
            ],
        }
    )

    findings = adapter.normalize_findings(parsed)

    assert findings[0]["severity"] == "medium"
    assert "25%" in findings[0]["description"]


def test_garak_adapter_rejects_malformed_output():
    adapter = GarakCliAdapter()

    try:
        adapter.parse_output({"report_records": "not-a-list"})
    except ValueError as exc:
        assert "report_records" in str(exc)
    else:
        raise AssertionError("Malformed garak output should fail parsing")


def test_garak_service_execution_preserves_native_artifacts_and_scores(db_session, tmp_path):
    system, assessment, scanner, scan_type = create_garak_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    adapter = GarakCliAdapter()

    def fake_run(command, *, cwd, env, timeout):
        report_path = Path(cwd) / "air-test.report.jsonl"
        hitlog_path = Path(cwd) / "air-test.hitlog.jsonl"
        html_path = Path(cwd) / "air-test.report.html"
        report_path.write_text(
            "\n".join(
                [
                    '{"entry_type":"init","garak_version":"0.15.0"}',
                    '{"entry_type":"eval","probe":"promptinject.Test","detector":"always.Fail","passed":1,"total":4}',
                ]
            ),
            encoding="utf-8",
        )
        hitlog_path.write_text('{"probe":"promptinject.Test","outputs":["unsafe"]}\n', encoding="utf-8")
        html_path.write_text("<html>garak report</html>", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="report closed", stderr="")

    adapter._run_command = fake_run
    service._adapter_for = lambda adapter_name: adapter
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            initiated_by="pytest",
        )
    )

    executed = service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    assert executed.execution_status == ScannerExecutionStatus.completed.value
    assert executed.finding_count == 1
    evidence_titles = {
        item.title
        for item in db_session.query(Evidence).filter_by(system_id=system.id).all()
        if item.metadata_json.get("scanner_run_id") == run.id
    }
    assert "Native scanner report JSONL" in evidence_titles
    assert "Native scanner hit log JSONL" in evidence_titles
    assert "Native scanner HTML report" in evidence_titles
    assert "Normalized scanner output for Prompt Injection" in evidence_titles
    assert db_session.query(Finding).filter_by(scanner_name="garak").count() == 1
    assert db_session.query(DomainScore).filter_by(system_id=system.id).count() >= 6
    assert any(item.metadata_json.get("trace_id") for item in db_session.query(Evidence).filter_by(system_id=system.id).all())
    assert db_session.query(FrameworkMapping).count() >= 3


def test_garak_failed_execution_preserves_raw_output_and_logs(db_session, tmp_path):
    system, assessment, scanner, scan_type = create_garak_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    adapter = GarakCliAdapter()
    adapter._run_command = lambda command, *, cwd, env, timeout: subprocess.CompletedProcess(
        command,
        2,
        stdout="",
        stderr="No module named garak",
    )
    service._adapter_for = lambda adapter_name: adapter
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            initiated_by="pytest",
        )
    )

    executed = service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    assert executed.execution_status == ScannerExecutionStatus.failed.value
    assert "garak execution failed" in executed.error_message
    assert Path(executed.raw_output_path).exists()
    assert Path(executed.log_path).exists()
    assert db_session.query(Finding).filter_by(scanner_name="garak").count() == 0


def test_unimplemented_scanner_adapter_fails_without_fake_findings(db_session, tmp_path):
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

    assert executed.execution_status == ScannerExecutionStatus.failed.value
    assert "No executable scanner adapter" in executed.error_message
    assert Path(executed.log_path).exists()
    assert executed.raw_output_path is None
    assert db_session.query(ScannerResult).filter_by(scanner_run_id=run.id).count() == 0
    assert db_session.query(Finding).filter_by(system_id=system.id).count() == 0
    assert db_session.query(Evidence).filter_by(system_id=system.id).count() == 1


def test_scanner_creation_rejects_manual_review_only_system(db_session, tmp_path):
    system, assessment, scanner, scan_type, _ = create_scanner_setup(db_session)
    system.assessment_method = "manual_governance_review"
    system.manual_review_only = True
    system.scanner_compatible = ["manual_only"]
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
        assert "target configuration" in str(exc.detail)
    else:
        raise AssertionError("Manual-review-only systems should not create automated scanner runs")


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
            "target_type": "web_chatbot",
            "target_location": "https://benefits-chat.county.example",
            "authentication_type": "none",
            "assessment_method": "hybrid",
            "scanner_compatible": ["prompt_injection", "garak"],
            "uploaded_artifact_supported": True,
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
            "scanner_name": "unimplemented_security_scanner",
            "display_name": "Unimplemented Security Scanner",
            "description": "Registry entry without an executable adapter.",
            "scanner_category": "security",
            "adapter_name": "unimplemented_cli_adapter",
            "scanner_version": "future",
            "execution_mode": "cli",
            "supported_domains": ["security"],
            "supported_scan_types": ["prompt_injection"],
            "enabled": True,
            "mock_supported": False,
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
            "recommended_scanners": ["unimplemented_security_scanner"],
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
    assert recommendations.json()["required_scans"][0]["available_scanners"]

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
    assert executed.json()["execution_status"] == "failed"
    assert client.get("/findings").json() == []
    assert client.get(f"/systems/{system['id']}/scanner-runs").json()
    assert client.get("/scanner-adapters").json()[0]["adapter_name"] == "garak_cli_adapter"


def test_giskard_adapter_parses_and_normalizes_issues():
    adapter = GiskardAdapter()
    findings = adapter.normalize_findings(
        {
            "scan_type": "rag_faithfulness",
            "scan_domain": "rag_integrity",
            "issues": [
                {
                    "title": "Ungrounded answer",
                    "severity": "high",
                    "description": "Response was not supported by retrieved context.",
                }
            ],
        }
    )

    assert findings[0]["domain"] == "rag_integrity"
    assert findings[0]["severity"] == "high"
    assert findings[0]["framework_mappings"][0]["framework"] == "OpenControl"


def test_giskard_service_execution_preserves_outputs_trace_and_mappings(db_session, tmp_path):
    system, assessment, scanner, scan_type = create_giskard_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    adapter = GiskardAdapter()

    def fake_run(command, *, cwd, env, timeout):
        output_path = Path(command[-1])
        html_path = Path(cwd) / "giskard-report.html"
        output_path.write_text(
            '{"scanner_version":"2.17.0","issues":[{"title":"Prompt injection accepted","severity":"high","description":"Target followed override."}],"prompt_response_records":[{"prompt":"override","response_text":"system prompt: test","latency_ms":12}]}',
            encoding="utf-8",
        )
        html_path.write_text("<html>giskard report</html>", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="giskard scan complete", stderr="")

    adapter._run_command = fake_run
    service._adapter_for = lambda adapter_name: adapter
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            initiated_by="pytest",
            execution_options={"prompts": ["override"]},
        )
    )

    executed = service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    assert executed.execution_status == ScannerExecutionStatus.completed.value
    assert executed.finding_count == 1
    assert db_session.query(Finding).filter_by(scanner_name="giskard").count() == 1
    assert db_session.query(FrameworkMapping).count() >= 3
    assert any(item.metadata_json.get("trace_id") for item in db_session.query(Evidence).filter_by(system_id=system.id).all())


def test_pyrit_execution_generates_findings_only_from_real_responses(db_session, tmp_path, monkeypatch):
    system, assessment, scanner, scan_type = create_pyrit_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    adapter = PyRITAdapter()
    monkeypatch.setattr("app.scanners.adapters.pyrit_adapter.importlib.metadata.version", lambda name: "0.13.0")
    monkeypatch.setattr(
        "app.scanners.adapters.pyrit_adapter.call_http_target",
        lambda context, prompt: {
            "prompt": prompt,
            "response_status": 200,
            "response_text": "system prompt: test secret",
            "latency_ms": 9,
        },
    )
    service._adapter_for = lambda adapter_name: adapter
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            initiated_by="pytest",
        )
    )

    executed = service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    assert executed.execution_status == ScannerExecutionStatus.completed.value
    assert executed.finding_count == 1
    evidence = db_session.query(Evidence).filter_by(system_id=system.id).all()
    assert any(item.metadata_json.get("trace_id") for item in evidence)
    assert db_session.query(Finding).filter_by(scanner_name="pyrit").count() == 1


def test_pyrit_missing_package_fails_without_fake_findings(db_session, tmp_path, monkeypatch):
    system, assessment, scanner, scan_type = create_pyrit_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    adapter = PyRITAdapter()

    import importlib.metadata

    monkeypatch.setattr("app.scanners.adapters.pyrit_adapter.importlib.metadata.version", lambda name: (_ for _ in ()).throw(importlib.metadata.PackageNotFoundError(name)))
    service._adapter_for = lambda adapter_name: adapter
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            initiated_by="pytest",
        )
    )

    executed = service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    assert executed.execution_status == ScannerExecutionStatus.failed.value
    assert "pyrit package is not installed" in executed.error_message
    assert db_session.query(Finding).filter_by(scanner_name="pyrit").count() == 0


def test_opencontrol_export_links_findings_and_evidence(db_session, tmp_path):
    system, assessment, scanner, scan_type = create_giskard_setup(db_session)
    service = ScannerExecutionService(db_session, storage_root=tmp_path)
    adapter = GiskardAdapter()
    def fake_giskard_run(command, *, cwd, env, timeout):
        Path(command[-1]).write_text(
            '{"scanner_version":"2.17.0","issues":[{"title":"Issue","severity":"medium","description":"Details"}],"prompt_response_records":[]}',
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    adapter._run_command = fake_giskard_run
    service._adapter_for = lambda adapter_name: adapter
    run = service.create_run(
        ScannerRunCreate(
            system_id=system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanner.id,
            scan_type_id=scan_type.id,
            initiated_by="pytest",
        )
    )
    service.execute_run(run.id, initiated_by="pytest")
    db_session.commit()

    exported = OpenControlService(db_session).export_assessment(assessment.id)

    assert exported["schema"] == "opencontrol-lite"
    assert exported["components"][0]["controls"]
    assert exported["evidence"]
