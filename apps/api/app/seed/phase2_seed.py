from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ai_system import AISystem
from app.models.audit_event import AuditEvent
from app.models.owner import Owner


OWNER_SPECS = [
    ("Maya Johnson", "maya.johnson@county.example", "County IT", "AI assurance operator"),
    ("Luis Ramirez", "luis.ramirez@county.example", "Civil Rights Office", "Civil-rights reviewer"),
    ("Priya Shah", "priya.shah@county.example", "Information Security", "Security reviewer"),
]


SYSTEM_SPECS = [
    {
        "system_name": "Public Benefits Chatbot",
        "department_owner": "Health and Human Services",
        "business_purpose": "Answers public benefits questions and routes residents to application support.",
        "public_facing": True,
        "rights_impacting": True,
        "uses_pii": True,
        "model_provider": "OpenAI",
        "model_version": "example-gpt-4.1",
        "deployment_environment": "pilot",
        "risk_tier": "high",
        "approval_status": "under_review",
        "target_type": "web_chatbot",
        "target_location": "https://benefits-chat.county.example",
        "authentication_type": "none",
        "assessment_method": "hybrid",
        "scanner_compatible": ["garak", "prompt_injection", "jailbreak"],
        "manual_review_only": False,
        "uploaded_artifact_supported": True,
    },
    {
        "system_name": "Sheriff Incident Summary Assistant",
        "department_owner": "Sheriff",
        "business_purpose": "Drafts internal incident report summaries for deputy review.",
        "rights_impacting": True,
        "safety_impacting": True,
        "uses_pii": True,
        "uses_cjis": True,
        "model_provider": "Azure OpenAI",
        "model_version": "example-gpt-4o",
        "deployment_environment": "internal",
        "risk_tier": "critical",
        "approval_status": "under_review",
        "target_type": "agent",
        "target_location": "http://internal-api:8000/incident-summary",
        "authentication_type": "bearer_token",
        "authentication_reference": "County IT scanner token record",
        "assessment_method": "hybrid",
        "scanner_compatible": ["garak", "prompt_injection", "jailbreak"],
        "manual_review_only": False,
        "uploaded_artifact_supported": True,
    },
    {
        "system_name": "Permit Review Assistant",
        "department_owner": "Planning and Permits",
        "business_purpose": "Summarizes permit applications and highlights missing materials.",
        "uses_pii": True,
        "model_provider": "Anthropic",
        "model_version": "example-claude",
        "deployment_environment": "pilot",
        "risk_tier": "moderate",
        "approval_status": "draft",
        "target_type": "uploaded_documents",
        "target_location": "uploaded permit packets",
        "authentication_type": "none",
        "assessment_method": "manual_governance_review",
        "scanner_compatible": ["manual_only"],
        "manual_review_only": True,
        "uploaded_artifact_supported": True,
    },
    {
        "system_name": "HR Resume Screening AI",
        "department_owner": "Human Resources",
        "business_purpose": "Assists HR staff with resume triage for county job postings.",
        "rights_impacting": True,
        "uses_pii": True,
        "model_provider": "Vendor model",
        "model_version": "example-2026.1",
        "deployment_environment": "vendor_sandbox",
        "risk_tier": "high",
        "approval_status": "under_review",
        "target_type": "vendor_ai",
        "target_location": "vendor AI sandbox portal",
        "authentication_type": "uploaded_credentials",
        "authentication_reference": "HR vendor assessment credentials file",
        "assessment_method": "manual_governance_review",
        "scanner_compatible": ["manual_only"],
        "manual_review_only": True,
        "uploaded_artifact_supported": True,
    },
    {
        "system_name": "Citizen Services RAG Chatbot",
        "department_owner": "County Manager",
        "business_purpose": "Retrieves county policy answers from approved public documents.",
        "public_facing": True,
        "model_provider": "OpenAI",
        "model_version": "example-gpt-4.1-mini",
        "deployment_environment": "pilot",
        "risk_tier": "moderate",
        "approval_status": "draft",
        "target_type": "rag_endpoint",
        "target_location": "http://internal-api:8000/rag/chat",
        "authentication_type": "api_key",
        "authentication_reference": "County Manager test API key record",
        "assessment_method": "hybrid",
        "scanner_compatible": ["garak", "prompt_injection"],
        "manual_review_only": False,
        "uploaded_artifact_supported": True,
    },
]


def seed_phase2(db: Session) -> None:
    _seed_owners(db)
    _seed_systems(db)
    db.flush()
    db.commit()


def _seed_owners(db: Session) -> None:
    existing = {item.email: item for item in db.scalars(select(Owner)).all()}
    for display_name, email, department, role in OWNER_SPECS:
        if email in existing:
            continue
        db.add(
            Owner(
                display_name=display_name,
                email=email,
                department=department,
                role=role,
            )
        )


def _seed_systems(db: Session) -> None:
    existing = {item.system_name: item for item in db.scalars(select(AISystem)).all()}
    for spec in SYSTEM_SPECS:
        system = existing.get(spec["system_name"])
        if system:
            for key, value in _with_defaults(spec).items():
                setattr(system, key, value)
            continue
        system = AISystem(**_with_defaults(spec))
        db.add(system)
        db.flush()
        db.add(
            AuditEvent(
                entity_type="system",
                entity_id=system.id,
                event_type="system_created",
                actor="seed",
                new_value=system.system_name,
                notes="Bootstrap example AI system. No assessment findings or evidence were seeded.",
            )
        )


def _with_defaults(spec: dict) -> dict:
    defaults = {
        "public_facing": False,
        "rights_impacting": False,
        "safety_impacting": False,
        "uses_pii": False,
        "uses_phi": False,
        "uses_cjis": False,
        "authentication_reference": None,
    }
    return {**defaults, **spec}


def recalculate_seed_scores(db: Session) -> None:
    return None
