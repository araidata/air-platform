from datetime import datetime
from typing import List, Optional

from pydantic import Field, model_validator

from app.schemas.base import ApiModel, StrictApiModel
from app.schemas.evidence import EvidenceRead
from app.schemas.finding import FindingRead
from app.schemas.scanner import AssessmentProfileRead


SUPPORTED_LANGUAGE_PAIRS = {("English", "Spanish"), ("Spanish", "English")}
APPEAL_CHECK_STATUSES = {
    "not_started",
    "needs_evidence",
    "under_review",
    "validated",
    "gap_found",
}


class LanguageAccessScenarioCreate(StrictApiModel):
    system_id: Optional[str] = None
    assessment_id: Optional[str] = None
    name: str
    primary_language: str = "English"
    comparison_language: str = "Spanish"
    scenario_type: str
    prompt_text: str
    expected_behavior: str
    evidence_requirements: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_language_pair(self):
        pair = (self.primary_language, self.comparison_language)
        if pair not in SUPPORTED_LANGUAGE_PAIRS:
            raise ValueError("language access scenarios currently support English/Spanish pairs")
        if self.primary_language == self.comparison_language:
            raise ValueError("comparison_language must differ from primary_language")
        return self


class LanguageAccessScenarioRead(ApiModel):
    id: str
    system_id: Optional[str]
    assessment_id: Optional[str]
    name: str
    primary_language: str
    comparison_language: str
    scenario_type: str
    prompt_text: str
    expected_behavior: str
    evidence_requirements: List[str]
    created_at: datetime
    updated_at: datetime


class HumanAppealPathCheckCreate(StrictApiModel):
    system_id: str
    assessment_id: Optional[str] = None
    check_type: str
    status: str = "needs_evidence"
    required_control: str
    validation_notes: Optional[str] = None
    evidence_requirements: List[str] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_check_state(self):
        if self.status not in APPEAL_CHECK_STATUSES:
            raise ValueError(f"unsupported appeal path check status: {self.status}")
        if self.status == "validated" and not self.evidence_ids:
            raise ValueError("validated appeal path checks require at least one evidence_id")
        return self


class HumanAppealPathCheckRead(ApiModel):
    id: str
    system_id: str
    assessment_id: Optional[str]
    check_type: str
    status: str
    required_control: str
    validation_notes: Optional[str]
    evidence_requirements: List[str]
    evidence_ids: List[str]
    created_at: datetime
    updated_at: datetime


class CivilRightsSummary(ApiModel):
    templates: List[AssessmentProfileRead]
    language_access_scenarios: List[LanguageAccessScenarioRead]
    appeal_path_checks: List[HumanAppealPathCheckRead]
    fairness_findings: List[FindingRead]
    fairness_evidence: List[EvidenceRead]
