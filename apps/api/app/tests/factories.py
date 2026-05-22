from app.models.ai_system import AISystem
from app.models.assessment import Assessment
from app.models.owner import Owner


def create_owner(db):
    owner = Owner(
        display_name="Maya Johnson",
        email="maya.johnson@county.example",
        department="County IT",
        role="AI assurance operator",
    )
    db.add(owner)
    db.flush()
    return owner


def create_system(db):
    system = AISystem(
        system_name="Public Benefits Chatbot",
        department_owner="Health and Human Services",
        business_purpose="Answers public benefits questions.",
        public_facing=True,
        rights_impacting=True,
        safety_impacting=False,
        uses_pii=True,
        uses_phi=False,
        uses_cjis=False,
        model_provider="OpenAI",
        model_version="mock",
        deployment_environment="pilot",
        risk_tier="high",
        approval_status="under_review",
    )
    db.add(system)
    db.flush()
    return system


def create_assessment(db, system):
    assessment = Assessment(
        system_id=system.id,
        assessment_type="AI assurance baseline",
        initiated_by="Maya Johnson",
        status="draft",
        summary="Baseline review.",
    )
    db.add(assessment)
    db.flush()
    return assessment
