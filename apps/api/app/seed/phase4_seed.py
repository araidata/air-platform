from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.assessment_profile import AssessmentProfile
from app.models.scan_type import ScanType
from app.models.scanner_definition import ScannerDefinition


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
    ("hallucination", "Hallucination", "explainability", "medium", ["moderate", "high", "critical"]),
    ("rag_faithfulness", "RAG Faithfulness", "rag_integrity", "high", ["moderate", "high", "critical"]),
    ("business_rule_validation", "Business Rule Validation", "governance", "medium", ["moderate", "high", "critical"]),
    ("multi_turn_adversarial", "Multi-Turn Adversarial", "security", "high", ["high", "critical"]),
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


SCANNER_DEFINITIONS = [
    ("garak", "garak", "security", "garak_cli_adapter", "cli", True, ["security"], ["prompt_injection", "jailbreak_resistance", "system_prompt_leakage"]),
    ("agentseal", "AgentSeal", "agent_safety", "agentseal_cli_adapter", "cli", False, ["agent_safety", "security"], ["unsafe_tool_use", "mcp_tool_poisoning"]),
    ("pyrit", "PyRIT", "security", "pyrit_adapter", "python", True, ["security"], ["prompt_injection", "jailbreak_resistance", "toxicity_unsafe_content", "data_exfiltration", "multi_turn_adversarial"]),
    ("modelscan", "ModelScan", "model_integrity", "modelscan_cli_adapter", "cli", False, ["supply_chain", "model_integrity"], ["unsafe_model_file", "dependency_risk", "unverified_model_origin"]),
    ("fairlearn", "Fairlearn", "bias_civil_rights", "fairlearn_import_adapter", "manual_import", False, ["bias_civil_rights"], ["protected_class_disparity"]),
    ("aequitas", "Aequitas", "bias_civil_rights", "aequitas_import_adapter", "manual_import", False, ["bias_civil_rights"], ["protected_class_disparity"]),
    ("ibm_aif360", "IBM AI Fairness 360", "bias_civil_rights", "aif360_import_adapter", "manual_import", False, ["bias_civil_rights"], ["protected_class_disparity"]),
    ("giskard", "Giskard", "ai_quality", "giskard_adapter", "python", True, ["bias_civil_rights", "explainability", "rag_integrity", "security", "governance"], ["hallucination", "protected_class_disparity", "prompt_injection", "rag_faithfulness", "rag_poisoning", "business_rule_validation", "missing_decision_rationale"]),
    ("ragas", "Ragas", "rag_integrity", "ragas_cli_adapter", "cli", False, ["rag_integrity"], ["rag_poisoning"]),
    ("deepeval", "DeepEval", "rag_integrity", "deepeval_cli_adapter", "cli", False, ["rag_integrity", "explainability"], ["rag_poisoning", "missing_decision_rationale"]),
    ("promptfoo", "Promptfoo", "security", "promptfoo_cli_adapter", "cli", False, ["security", "rag_integrity"], ["prompt_injection", "jailbreak_resistance", "rag_poisoning"]),
]


PROFILES = [
    ("Public-Facing Chatbot Review", ["high", "moderate"], ["public_facing"], ["prompt_injection", "pii_leakage", "language_access_disparity", "human_appeal_path_missing", "missing_approval"], ["jailbreak_resistance", "missing_decision_rationale"], ["raw scanner output", "prompt transcripts", "appeal path evidence"], ["garak"], ["security", "privacy", "bias_civil_rights", "governance_evidence"]),
    ("Rights-Impacting AI Review", ["high", "critical"], ["rights_impacting"], ["protected_class_disparity", "human_appeal_path_missing", "adverse_decision_explanation_gap", "missing_policy_mapping"], ["language_access_disparity", "missing_confidence_disclosure"], ["civil-rights scenario evidence", "human appeal evidence"], [], ["bias_civil_rights", "explainability", "governance_evidence"]),
    ("Law Enforcement / CJIS AI Review", ["critical"], ["cjis", "safety_impacting"], ["cjis_data_exposure", "unsafe_tool_use", "missing_audit_evidence", "missing_decision_rationale"], ["data_exfiltration", "mcp_tool_poisoning"], ["CJIS handling evidence", "audit logs", "tool permission evidence"], [], ["security", "privacy", "governance_evidence"]),
    ("HR / Employment AI Review", ["high"], ["rights_impacting"], ["protected_class_disparity", "human_appeal_path_missing", "adverse_decision_explanation_gap"], ["missing_confidence_disclosure"], ["selection criteria evidence", "appeal path evidence"], [], ["bias_civil_rights", "explainability"]),
    ("RAG Application Review", ["moderate", "high"], ["rag"], ["rag_poisoning", "prompt_injection", "missing_policy_mapping"], ["data_exfiltration", "missing_decision_rationale"], ["corpus manifest", "retrieval transcript", "raw scanner output"], ["garak"], ["security", "rag_integrity", "governance_evidence"]),
    ("Agentic AI / Tool-Using AI Review", ["high", "critical"], ["agentic"], ["unsafe_tool_use", "mcp_tool_poisoning", "data_exfiltration", "missing_audit_evidence"], ["prompt_injection"], ["tool inventory", "approval log", "raw scanner output"], [], ["security", "governance_evidence"]),
    ("Low-Risk Internal AI Review", ["low", "moderate"], ["internal"], ["missing_owner", "missing_approval"], ["retention_policy_gap", "missing_decision_rationale"], ["owner attestation", "approval note"], [], ["governance_evidence"]),
]


def seed_phase4(db: Session) -> None:
    _seed_scan_types(db)
    _seed_scanner_definitions(db)
    _seed_profiles(db)
    db.flush()
    db.commit()


def _seed_scan_types(db: Session) -> None:
    existing = {item.name: item for item in db.scalars(select(ScanType)).all()}
    for name, display, domain, severity, tiers in SCAN_TYPES:
        data = {
            "display_name": display,
            "description": f"Assessment control for {display.lower()} in the {domain.replace('_', ' ')} domain.",
            "domain": domain,
            "default_severity": severity,
            "required_for_risk_tiers": tiers,
            "applicable_system_types": ["public_facing", "rights_impacting", "internal", "rag", "agentic"],
            "evidence_expectations": ["real scanner output", "execution log", "operator-collected evidence"],
            "enabled": True,
        }
        item = existing.get(name)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            continue
        db.add(ScanType(name=name, **data))


def _seed_scanner_definitions(db: Session) -> None:
    existing = {item.scanner_name: item for item in db.scalars(select(ScannerDefinition)).all()}
    for name, display, category, adapter, mode, enabled, domains, scan_types in SCANNER_DEFINITIONS:
        data = {
            "display_name": display,
            "description": f"{display} registry entry for {category.replace('_', ' ')} assessment workflows.",
            "scanner_category": category,
            "adapter_name": adapter,
            "scanner_version": _scanner_version(name),
            "execution_mode": mode,
            "supported_domains": domains,
            "supported_scan_types": scan_types,
            "enabled": enabled,
            "mock_supported": False,
            "requires_credentials": False,
        }
        item = existing.get(name)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            continue
        db.add(ScannerDefinition(scanner_name=name, **data))


def _scanner_version(name: str) -> str:
    return {
        "garak": "0.15.x",
        "giskard": "2.x",
        "pyrit": "0.13.x",
    }.get(name, "future")


def _seed_profiles(db: Session) -> None:
    existing = {item.profile_name: item for item in db.scalars(select(AssessmentProfile)).all()}
    for name, tiers, system_types, required, optional, evidence, scanners, score_domains in PROFILES:
        data = {
            "description": f"Operational assessment profile for {name.lower()}.",
            "applicable_risk_tiers": tiers,
            "applicable_system_types": system_types,
            "required_scan_types": required,
            "optional_scan_types": optional,
            "required_evidence_types": evidence,
            "recommended_scanners": scanners,
            "governance_expectations": [
                "Preserve real scanner output and execution logs.",
                "Normalize only actual scanner findings into platform workflow.",
                "Link operator-collected evidence to assessments and findings.",
            ],
            "score_domains_affected": score_domains,
            "enabled": True,
        }
        item = existing.get(name)
        if item:
            for key, value in data.items():
                setattr(item, key, value)
            continue
        db.add(AssessmentProfile(profile_name=name, **data))
