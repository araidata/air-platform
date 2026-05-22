from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class ScannerExecutionContext:
    run_id: str
    system_id: str
    system_name: str
    risk_tier: str
    scan_type: str
    scan_domain: str
    profile_name: str | None = None


@dataclass(frozen=True)
class ScannerExecutionResult:
    status: str
    raw_output: dict[str, Any]
    logs: str
    error_message: str | None = None
    artifacts: dict[str, Any] = field(default_factory=dict)


class ScannerAdapter(Protocol):
    def get_name(self) -> str:
        ...

    def get_version(self) -> str:
        ...

    def validate_configuration(self, context: ScannerExecutionContext) -> None:
        ...

    def execute(self, context: ScannerExecutionContext) -> ScannerExecutionResult:
        ...

    def parse_output(self, raw_output: dict[str, Any]) -> dict[str, Any]:
        ...

    def normalize_findings(self, parsed_output: dict[str, Any]) -> list[dict[str, Any]]:
        ...

    def generate_evidence(self, parsed_output: dict[str, Any]) -> list[dict[str, Any]]:
        ...
