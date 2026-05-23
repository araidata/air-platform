from datetime import datetime
from typing import Literal, Optional

from pydantic import Field

from app.schemas.base import ApiModel, StrictApiModel


TargetType = Literal[
    "web_chatbot",
    "rest_api",
    "rag_endpoint",
    "agent",
    "local_model",
    "vendor_ai",
    "uploaded_prompts",
    "uploaded_documents",
    "manual_review_only",
]
AuthenticationType = Literal["none", "bearer_token", "api_key", "session_auth", "uploaded_credentials"]
AssessmentMethod = Literal["automated_scan", "manual_governance_review", "hybrid"]


class AISystemCreate(StrictApiModel):
    system_name: str
    department_owner: str
    business_purpose: str
    public_facing: bool = False
    rights_impacting: bool = False
    safety_impacting: bool = False
    uses_pii: bool = False
    uses_phi: bool = False
    uses_cjis: bool = False
    model_provider: Optional[str] = None
    model_version: Optional[str] = None
    deployment_environment: str = "pilot"
    risk_tier: str = "moderate"
    approval_status: str = "pending"
    target_type: TargetType = "manual_review_only"
    target_location: str = "manual review packet"
    authentication_type: AuthenticationType = "none"
    authentication_reference: Optional[str] = None
    assessment_method: AssessmentMethod = "manual_governance_review"
    scanner_compatible: list[str] = Field(default_factory=list)
    manual_review_only: bool = False
    uploaded_artifact_supported: bool = False


class AISystemUpdate(StrictApiModel):
    system_name: Optional[str] = None
    department_owner: Optional[str] = None
    business_purpose: Optional[str] = None
    public_facing: Optional[bool] = None
    rights_impacting: Optional[bool] = None
    safety_impacting: Optional[bool] = None
    uses_pii: Optional[bool] = None
    uses_phi: Optional[bool] = None
    uses_cjis: Optional[bool] = None
    model_provider: Optional[str] = None
    model_version: Optional[str] = None
    deployment_environment: Optional[str] = None
    risk_tier: Optional[str] = None
    approval_status: Optional[str] = None
    target_type: Optional[TargetType] = None
    target_location: Optional[str] = None
    authentication_type: Optional[AuthenticationType] = None
    authentication_reference: Optional[str] = None
    assessment_method: Optional[AssessmentMethod] = None
    scanner_compatible: Optional[list[str]] = None
    manual_review_only: Optional[bool] = None
    uploaded_artifact_supported: Optional[bool] = None


class AISystemRead(ApiModel):
    id: str
    system_name: str
    department_owner: str
    business_purpose: str
    public_facing: bool
    rights_impacting: bool
    safety_impacting: bool
    uses_pii: bool
    uses_phi: bool
    uses_cjis: bool
    model_provider: Optional[str]
    model_version: Optional[str]
    deployment_environment: str
    risk_tier: str
    approval_status: str
    target_type: str
    target_location: str
    authentication_type: str
    authentication_reference: Optional[str]
    assessment_method: str
    scanner_compatible: list[str]
    manual_review_only: bool
    uploaded_artifact_supported: bool
    created_at: datetime
    updated_at: datetime
