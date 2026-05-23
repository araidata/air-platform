from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import Field, field_validator, model_validator

from app.schemas.base import ApiModel, StrictApiModel


AssessmentToolEngine = Literal["garak", "http_tester"]
AssessmentToolTest = Literal[
    "prompt_injection",
    "jailbreak",
    "system_prompt_leakage",
    "encoding_obfuscation",
    "toxicity_unsafe_content",
    "pii_leakage",
    "policy_bypass",
]


class AssessmentToolRunCreate(StrictApiModel):
    engine: AssessmentToolEngine
    target_name: str = "Assessment target"
    target_url: str
    method: Literal["GET", "POST"] = "POST"
    request_template: Dict[str, Any] = Field(default_factory=lambda: {"prompt": "{{prompt}}"})
    response_path: str = "response"
    auth_header_name: Optional[str] = None
    auth_header_value: Optional[str] = None
    selected_tests: List[AssessmentToolTest] = Field(default_factory=lambda: ["prompt_injection"])
    generations: int = Field(default=1, ge=1, le=5)
    timeout_seconds: int = Field(default=60, ge=5, le=300)

    @field_validator("target_url")
    @classmethod
    def target_url_must_be_http(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            raise ValueError("Target URL must start with http:// or https://")
        return value

    @model_validator(mode="after")
    def validate_template_and_auth(self) -> "AssessmentToolRunCreate":
        if "{{prompt}}" not in str(self.request_template):
            raise ValueError("Request template must include {{prompt}}")
        if bool(self.auth_header_name) != bool(self.auth_header_value):
            raise ValueError("Auth header name and value must be provided together")
        return self


class AssessmentToolFinding(ApiModel):
    id: str
    test: str
    severity: str
    title: str
    rationale: str
    prompt: str
    response_excerpt: str
    remediation: str


class AssessmentToolStep(ApiModel):
    label: str
    status: str
    detail: str
    timestamp: str


class AssessmentToolRunRead(ApiModel):
    id: str
    engine: str
    status: str
    target_name: str
    target_url: str
    method: str
    selected_tests: List[str]
    request_template: Dict[str, Any]
    response_path: str
    request_headers: Dict[str, Any]
    steps: List[Dict[str, Any]]
    findings: List[Dict[str, Any]]
    report: Dict[str, Any]
    artifacts: Dict[str, Any]
    error_message: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
