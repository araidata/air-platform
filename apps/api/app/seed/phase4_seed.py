from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai_system import AISystem
from app.models.assessment import Assessment
from app.models.assessment_profile import AssessmentProfile
from app.models.scan_type import ScanType
from app.models.scanner_definition import ScannerDefinition
from app.models.scanner_run import ScannerRun
from app.schemas.scanner import ScannerRunCreate
from app.scanners.services.scanner_execution_service import ScannerExecutionService


SCAN_TYPES = [
    ("prompt_injection", "Prompt Injection", "security", "high", ["high", "critical"]),
    ("jailbreak_resistance", "Jailbreak Resistance", "security", "high", ["high", "critical"]),
    ("system_prompt_leakage", "System Prompt Leakage", "security", "medium", ["high", "critical"]),
    ("unsafe_tool_use", "Unsafe Tool Use", "agent_safety", "critical", ["high", "critical"]),
    ("mcp_tool_poisoning", "MCP Tool Poisoning", "agent_safety", "high", ["critical"]),
    ("rag_poisoning", "RAG Poisoning", "rag_integrity", "high", ["moderate", "high", "critical"]),
    ("data_exfiltration", "Data Exfiltration", "security", "critical", ["high", "critical"]),
    ("pii_leakage", "PII Leakage", "privacy", "medium", ["moderate", "high", "critical"]),
    ("phi_leakage", "PHI Leakage", "privacy", "high", ["high", "critical"]),
    ("cjis_data_exposure", "CJIS Data Exposure", "privacy", "critical", ["critical"]),
    ("retention_policy_gap", "Retention Policy Gap", "privacy", "medium", ["moderate", "high", "critical"]),
    ("language_access_disparity", "Language Access Disparity", "bias_civil_rights", "high", ["high", "critical"]),
    ("protected_class_disparity", "Protected Class Disparity", "bias_civil_rights", "high", ["high", "critical"]),
    ("accessibility_disparity", "Accessibility Disparity", "bias_civil_rights", "medium", ["high", "critical"]),
    ("human_appeal_path_missing", "Human Appeal Path Missing", "governance", "high", ["high", "critical"]),
    ("adverse_decision_explanation_gap", "Adverse Decision Explanation Gap", "explainability", "high", ["high", "critical"]),
    ("missing_decision_rationale", "Missing Decision Rationale", "explainability", "medium", ["moderate", "high", "critical"]),
    ("missing_confidence_disclosure", "Missing Confidence Disclosure", "explainability", "medium", ["moderate", "high", "critical"]),
    ("opaque_escalation_logic", "Opaque Escalation Logic", "explainability", "medium", ["high", "critical"]),
    ("missing_approval", "Missing Approval", "governance", "medium", ["moderate", "high", "critical"]),
    ("missing_risk_acceptance", "Missing Risk Acceptance", "governance", "medium", ["moderate", "high", "critical"]),
    ("missing_audit_evidence", "Missing Audit Evidence", "governance", "medium", ["moderate", "high", "critical"]),
    ("missing_policy_mapping", "Missing Policy Mapping", "governance", "low", ["high", "critical"]),
    ("missing_owner", "Missing Owner", "governance", "medium", ["moderate", "high", "critical"]),
    ("unsafe_model_file", "Unsafe Model File", "supply_chain", "critical", ["high", "critical"]),
    ("dependency_risk", "Dependency Risk", "supply_chain", "high", ["high", "critical"]),
    ("unverified_model_origin", "Unverified Model Origin", "model_integrity", "high", ["high", "critical"]),
]


def seed_phase4(db: Session) -> None:
    scan_types = _seed_scan_types(db)
    scanners = _seed_scanner_definitions(db)
    profiles = _seed_profiles(db)
    db.flush()
    _seed_mock_runs(db, scan_types, scanners, profiles)
    db.commit()


def _seed_scan_types(db: Session) -> dict[str, ScanType]:
    existing = {item.name: item for item in db.scalars(select(ScanType)).all()}
    for name, display, domain, severity, tiers in SCAN_TYPES:
        if name in existing:
            continue
        scan_type = ScanType(
            name=name,
            display_name=display,
            description=f"Assessment control for {display.lower()} in the {domain.replace('_', ' ')} domain.",
            domain=domain,
            default_severity=severity,
            required_for_risk_tiers=tiers,
            applicable_system_types=["public_facing", "rights_impacting", "internal", "rag", "agentic"],
            evidence_expectations=[
                "raw scanner output",
                "execution log",
                "normalized finding evidence",
            ],
            enabled=True,
        )
        db.add(scan_type)
        existing[name] = scan_type
    db.flush()
    return existing


def _seed_scanner_definitions(db: Session) -> dict[str, ScannerDefinition]:
    existing = {item.scanner_name: item for item in db.scalars(select(ScannerDefinition)).all()}
    definitions = [
        ("mock_ai_security_scanner", "Mock AI Security Scanner", "security", "mock_adapter", "mock", True, ["security", "agent_safety", "rag_integrity"], ["prompt_injection", "jailbreak_resistance", "system_prompt_leakage", "unsafe_tool_use", "mcp_tool_poisoning", "rag_poisoning", "data_exfiltration"]),
        ("mock_bias_civil_rights_scanner", "Mock Bias & Civil Rights Scanner", "bias_civil_rights", "mock_adapter", "mock", True, ["bias_civil_rights", "governance"], ["language_access_disparity", "protected_class_disparity", "accessibility_disparity", "human_appeal_path_missing", "adverse_decision_explanation_gap"]),
        ("mock_governance_evidence_scanner", "Mock Governance Evidence Scanner", "governance", "mock_adapter", "mock", True, ["governance", "explainability"], ["missing_approval", "missing_risk_acceptance", "missing_audit_evidence", "missing_policy_mapping", "missing_owner", "missing_decision_rationale"]),
        ("garak", "garak", "security", "garak_cli_adapter", "cli", True, ["security"], ["prompt_injection", "jailbreak_resistance", "system_prompt_leakage"]),
        ("agentseal", "AgentSeal", "agent_safety", "agentseal_cli_adapter", "cli", False, ["agent_safety", "security"], ["unsafe_tool_use", "mcp_tool_poisoning"]),
        ("pyrit", "PyRIT", "security", "pyrit_cli_adapter", "cli", False, ["security"], ["prompt_injection", "jailbreak_resistance", "data_exfiltration"]),
        ("modelscan", "ModelScan", "model_integrity", "modelscan_cli_adapter", "cli", False, ["supply_chain", "model_integrity"], ["unsafe_model_file", "dependency_risk", "unverified_model_origin"]),
        ("fairlearn", "Fairlearn", "bias_civil_rights", "fairlearn_import_adapter", "manual_import", False, ["bias_civil_rights"], ["protected_class_disparity"]),
        ("aequitas", "Aequitas", "bias_civil_rights", "aequitas_import_adapter", "manual_import", False, ["bias_civil_rights"], ["protected_class_disparity"]),
        ("ibm_aif360", "IBM AI Fairness 360", "bias_civil_rights", "aif360_import_adapter", "manual_import", False, ["bias_civil_rights"], ["protected_class_disparity"]),
        ("giskard", "Giskard", "bias_civil_rights", "giskard_cli_adapter", "cli", False, ["bias_civil_rights", "explainability"], ["protected_class_disparity", "missing_decision_rationale"]),
        ("ragas", "Ragas", "rag_integrity", "ragas_cli_adapter", "cli", False, ["rag_integrity"], ["rag_poisoning"]),
        ("deepeval", "DeepEval", "rag_integrity", "deepeval_cli_adapter", "cli", False, ["rag_integrity", "explainability"], ["rag_poisoning", "missing_decision_rationale"]),
        ("promptfoo", "Promptfoo", "security", "promptfoo_cli_adapter", "cli", False, ["security", "rag_integrity"], ["prompt_injection", "jailbreak_resistance", "rag_poisoning"]),
    ]
    for name, display, category, adapter, mode, enabled, domains, scan_types in definitions:
        if name in existing:
            if name == "garak":
                scanner = existing[name]
                scanner.adapter_name = adapter
                scanner.scanner_version = "0.15.x"
                scanner.execution_mode = mode
                scanner.supported_domains = domains
                scanner.supported_scan_types = scan_types
                scanner.enabled = True
                scanner.mock_supported = False
            continue
        scanner = ScannerDefinition(
            scanner_name=name,
            display_name=display,
            description=f"{display} registry entry for future {category.replace('_', ' ')} assessment workflows.",
            scanner_category=category,
            adapter_name=adapter,
            scanner_version="0.15.x" if name == "garak" else ("future" if not enabled else "0.4.0"),
            execution_mode=mode,
            supported_domains=domains,
            supported_scan_types=scan_types,
            enabled=enabled,
            mock_supported=enabled and adapter == "mock_adapter",
            requires_credentials=False,
        )
        db.add(scanner)
        existing[name] = scanner
    db.flush()
    return existing


def _seed_profiles(db: Session) -> dict[str, AssessmentProfile]:
    existing = {item.profile_name: item for item in db.scalars(select(AssessmentProfile)).all()}
    profiles = [
        ("Public-Facing Chatbot Review", ["high", "moderate"], ["public_facing"], ["prompt_injection", "pii_leakage", "language_access_disparity", "human_appeal_path_missing", "missing_approval"], ["jailbreak_resistance", "missing_decision_rationale"], ["raw scanner output", "prompt transcripts", "appeal path evidence"], ["mock_ai_security_scanner", "mock_bias_civil_rights_scanner"], ["security", "privacy", "bias_civil_rights", "governance_evidence"]),
        ("Rights-Impacting AI Review", ["high", "critical"], ["rights_impacting"], ["protected_class_disparity", "human_appeal_path_missing", "adverse_decision_explanation_gap", "missing_policy_mapping"], ["language_access_disparity", "missing_confidence_disclosure"], ["civil-rights scenario evidence", "human appeal evidence"], ["mock_bias_civil_rights_scanner"], ["bias_civil_rights", "explainability", "governance_evidence"]),
        ("Law Enforcement / CJIS AI Review", ["critical"], ["cjis", "safety_impacting"], ["cjis_data_exposure", "unsafe_tool_use", "missing_audit_evidence", "missing_decision_rationale"], ["data_exfiltration", "mcp_tool_poisoning"], ["CJIS handling evidence", "audit logs", "tool permission evidence"], ["mock_ai_security_scanner", "mock_governance_evidence_scanner"], ["security", "privacy", "governance_evidence"]),
        ("HR / Employment AI Review", ["high"], ["rights_impacting"], ["protected_class_disparity", "human_appeal_path_missing", "adverse_decision_explanation_gap"], ["missing_confidence_disclosure"], ["selection criteria evidence", "appeal path evidence"], ["mock_bias_civil_rights_scanner"], ["bias_civil_rights", "explainability"]),
        ("RAG Application Review", ["moderate", "high"], ["rag"], ["rag_poisoning", "prompt_injection", "missing_policy_mapping"], ["data_exfiltration", "missing_decision_rationale"], ["corpus manifest", "retrieval transcript", "raw scanner output"], ["mock_ai_security_scanner"], ["security", "rag_integrity", "governance_evidence"]),
        ("Agentic AI / Tool-Using AI Review", ["high", "critical"], ["agentic"], ["unsafe_tool_use", "mcp_tool_poisoning", "data_exfiltration", "missing_audit_evidence"], ["prompt_injection"], ["tool inventory", "approval log", "raw scanner output"], ["mock_ai_security_scanner"], ["security", "governance_evidence"]),
        ("Low-Risk Internal AI Review", ["low", "moderate"], ["internal"], ["missing_owner", "missing_approval"], ["retention_policy_gap", "missing_decision_rationale"], ["owner attestation", "approval note"], ["mock_governance_evidence_scanner"], ["governance_evidence"]),
    ]
    for name, tiers, system_types, required, optional, evidence, scanners, score_domains in profiles:
        if name in existing:
            continue
        profile = AssessmentProfile(
            profile_name=name,
            description=f"Operational assessment profile for {name.lower()}.",
            applicable_risk_tiers=tiers,
            applicable_system_types=system_types,
            required_scan_types=required,
            optional_scan_types=optional,
            required_evidence_types=evidence,
            recommended_scanners=scanners,
            governance_expectations=[
                "Preserve raw output and execution logs.",
                "Normalize findings into platform workflow.",
                "Link evidence to assessment and findings.",
            ],
            score_domains_affected=score_domains,
            enabled=True,
        )
        db.add(profile)
        existing[name] = profile
    db.flush()
    return existing


def _seed_mock_runs(
    db: Session,
    scan_types: dict[str, ScanType],
    scanners: dict[str, ScannerDefinition],
    profiles: dict[str, AssessmentProfile],
) -> None:
    if db.scalar(select(ScannerRun).where(ScannerRun.scanner_name == "mock_ai_security_scanner")):
        return
    systems = {item.system_name: item for item in db.scalars(select(AISystem)).all()}
    service = ScannerExecutionService(db)
    plan = [
        ("Public Benefits Chatbot", "prompt_injection", "mock_ai_security_scanner", "Public-Facing Chatbot Review"),
        ("Sheriff Incident Summary Assistant", "unsafe_tool_use", "mock_ai_security_scanner", "Law Enforcement / CJIS AI Review"),
        ("Permit Review Assistant", "missing_approval", "mock_governance_evidence_scanner", "Low-Risk Internal AI Review"),
        ("HR Resume Screening AI", "human_appeal_path_missing", "mock_bias_civil_rights_scanner", "HR / Employment AI Review"),
        ("Citizen Services RAG Chatbot", "rag_poisoning", "mock_ai_security_scanner", "RAG Application Review"),
    ]
    for system_name, scan_type_name, scanner_name, profile_name in plan:
        system = systems.get(system_name)
        if not system:
            continue
        assessment = _latest_assessment(db, system) or Assessment(
            system_id=system.id,
            assessment_type=profile_name,
            initiated_by="seed",
            status="running",
            started_at=datetime.utcnow(),
            summary=f"Seeded {profile_name}.",
        )
        if not assessment.id:
            db.add(assessment)
            db.flush()
        run = service.create_run(
            ScannerRunCreate(
                system_id=system.id,
                assessment_id=assessment.id,
                scanner_definition_id=scanners[scanner_name].id,
                scan_type_id=scan_types[scan_type_name].id,
                assessment_profile_id=profiles[profile_name].id,
                initiated_by="seed",
            )
        )
        service.execute_run(run.id, initiated_by="seed")

    failed_system = systems.get("Citizen Services RAG Chatbot")
    if failed_system:
        assessment = _latest_assessment(db, failed_system)
        failed = ScannerRun(
            system_id=failed_system.id,
            assessment_id=assessment.id,
            scanner_definition_id=scanners["mock_governance_evidence_scanner"].id,
            scan_type_id=scan_types["missing_audit_evidence"].id,
            assessment_profile_id=profiles["RAG Application Review"].id,
            scanner_name="mock_governance_evidence_scanner",
            scanner_version="0.4.0",
            adapter_name="mock_adapter",
            execution_status="failed",
            initiated_by="seed",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            finding_count=0,
            error_message="Seeded failed run showing malformed assessment input handling.",
        )
        db.add(failed)


def _latest_assessment(db: Session, system: AISystem) -> Assessment | None:
    return db.scalar(
        select(Assessment)
        .where(Assessment.system_id == system.id)
        .order_by(Assessment.created_at.desc())
        .limit(1)
    )
