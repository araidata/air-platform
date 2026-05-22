from datetime import datetime
from typing import Optional

from app.schemas.base import ApiModel, StrictApiModel


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
    created_at: datetime
    updated_at: datetime
