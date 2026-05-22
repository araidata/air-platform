from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import Field

from app.schemas.base import ApiModel, StrictApiModel


class ScannerDefinitionCreate(StrictApiModel):
    scanner_name: str
    display_name: str
    description: str
    scanner_category: str
    adapter_name: str
    scanner_version: str = "0.1.0"
    execution_mode: str = "mock"
    supported_domains: List[str] = Field(default_factory=list)
    supported_scan_types: List[str] = Field(default_factory=list)
    enabled: bool = True
    mock_supported: bool = False
    requires_credentials: bool = False


class ScannerDefinitionUpdate(StrictApiModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    scanner_category: Optional[str] = None
    adapter_name: Optional[str] = None
    scanner_version: Optional[str] = None
    execution_mode: Optional[str] = None
    supported_domains: Optional[List[str]] = None
    supported_scan_types: Optional[List[str]] = None
    enabled: Optional[bool] = None
    mock_supported: Optional[bool] = None
    requires_credentials: Optional[bool] = None


class ScannerDefinitionRead(ApiModel):
    id: str
    scanner_name: str
    display_name: str
    description: str
    scanner_category: str
    adapter_name: str
    scanner_version: str
    execution_mode: str
    supported_domains: List[str]
    supported_scan_types: List[str]
    enabled: bool
    mock_supported: bool
    requires_credentials: bool
    created_at: datetime
    updated_at: datetime


class ScanTypeCreate(StrictApiModel):
    name: str
    display_name: str
    description: str
    domain: str
    default_severity: str = "medium"
    required_for_risk_tiers: List[str] = Field(default_factory=list)
    applicable_system_types: List[str] = Field(default_factory=list)
    evidence_expectations: List[str] = Field(default_factory=list)
    enabled: bool = True


class ScanTypeUpdate(StrictApiModel):
    display_name: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None
    default_severity: Optional[str] = None
    required_for_risk_tiers: Optional[List[str]] = None
    applicable_system_types: Optional[List[str]] = None
    evidence_expectations: Optional[List[str]] = None
    enabled: Optional[bool] = None


class ScanTypeRead(ApiModel):
    id: str
    name: str
    display_name: str
    description: str
    domain: str
    default_severity: str
    required_for_risk_tiers: List[str]
    applicable_system_types: List[str]
    evidence_expectations: List[str]
    enabled: bool
    created_at: datetime
    updated_at: datetime


class AssessmentProfileCreate(StrictApiModel):
    profile_name: str
    description: str
    applicable_risk_tiers: List[str] = Field(default_factory=list)
    applicable_system_types: List[str] = Field(default_factory=list)
    required_scan_types: List[str] = Field(default_factory=list)
    optional_scan_types: List[str] = Field(default_factory=list)
    required_evidence_types: List[str] = Field(default_factory=list)
    recommended_scanners: List[str] = Field(default_factory=list)
    governance_expectations: List[str] = Field(default_factory=list)
    score_domains_affected: List[str] = Field(default_factory=list)
    enabled: bool = True


class AssessmentProfileUpdate(StrictApiModel):
    description: Optional[str] = None
    applicable_risk_tiers: Optional[List[str]] = None
    applicable_system_types: Optional[List[str]] = None
    required_scan_types: Optional[List[str]] = None
    optional_scan_types: Optional[List[str]] = None
    required_evidence_types: Optional[List[str]] = None
    recommended_scanners: Optional[List[str]] = None
    governance_expectations: Optional[List[str]] = None
    score_domains_affected: Optional[List[str]] = None
    enabled: Optional[bool] = None


class AssessmentProfileRead(ApiModel):
    id: str
    profile_name: str
    description: str
    applicable_risk_tiers: List[str]
    applicable_system_types: List[str]
    required_scan_types: List[str]
    optional_scan_types: List[str]
    required_evidence_types: List[str]
    recommended_scanners: List[str]
    governance_expectations: List[str]
    score_domains_affected: List[str]
    enabled: bool
    created_at: datetime
    updated_at: datetime


class ScannerRunCreate(StrictApiModel):
    system_id: str
    assessment_id: Optional[str] = None
    scanner_definition_id: str
    scan_type_id: str
    assessment_profile_id: Optional[str] = None
    initiated_by: str = "operator"


class ScannerRunExecuteRequest(StrictApiModel):
    initiated_by: str = "operator"


class ScannerRunRead(ApiModel):
    id: str
    system_id: str
    assessment_id: str
    scanner_definition_id: str
    scan_type_id: str
    assessment_profile_id: Optional[str]
    scanner_name: str
    scanner_version: str
    adapter_name: str
    execution_status: str
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    initiated_by: str
    raw_output_path: Optional[str]
    log_path: Optional[str]
    finding_count: int
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime


class ScannerResultRead(ApiModel):
    id: str
    scanner_run_id: str
    raw_result_json: Dict[str, Any]
    normalized: Dict[str, Any]
    normalization_version: str
    created_at: datetime


class ScannerAdapterRead(ApiModel):
    adapter_name: str
    scanner_name: str
    scanner_version: str
    supported_execution_modes: List[str]
    supported_scan_types: List[str]
    mock_supported: bool


class RecommendedScan(ApiModel):
    scan_type: ScanTypeRead
    required: bool
    reason: str
    available_scanners: List[ScannerDefinitionRead]


class SystemScanRecommendations(ApiModel):
    system_id: str
    risk_tier: str
    assessment_profile: Optional[AssessmentProfileRead]
    required_scans: List[RecommendedScan]
    optional_scans: List[RecommendedScan]
