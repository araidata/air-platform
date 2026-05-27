from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from app.scanners.adapters.base import ScannerExecutionContext


DEFAULT_REQUEST_TEMPLATE = {"prompt": "{{prompt}}"}


def load_prompts(context: ScannerExecutionContext, defaults: list[str]) -> list[str]:
    configured = context.execution_options.get("prompts") or context.execution_options.get("evaluation_prompts")
    if isinstance(configured, str):
        configured = [line for line in configured.splitlines() if line.strip()]
    if isinstance(configured, list) and configured:
        return [str(item) for item in configured if str(item).strip()]
    return defaults


def call_http_target(context: ScannerExecutionContext, prompt: str) -> dict[str, Any]:
    if not context.target_location.startswith(("http://", "https://")):
        raise ValueError("scanner target requires an HTTP or HTTPS target_location")
    method = str(context.execution_options.get("method") or "POST").upper()
    request_template = context.execution_options.get("request_template") or DEFAULT_REQUEST_TEMPLATE
    response_path = str(context.execution_options.get("response_path") or "response")
    body = _replace_prompt(request_template, prompt)
    headers = {
        "Content-Type": "application/json",
        **{
            str(key): str(value)
            for key, value in (context.execution_options.get("headers") or {}).items()
            if value is not None
        },
    }
    auth_header_name = context.execution_options.get("auth_header_name")
    auth_header_value = context.execution_options.get("auth_header_value")
    if auth_header_name and auth_header_value:
        headers[str(auth_header_name)] = str(auth_header_value)

    encoded = None if method == "GET" else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        context.target_location,
        data=encoded,
        headers=headers,
        method=method,
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=int(context.execution_options.get("timeout_seconds", 30))) as response:
            raw = response.read().decode("utf-8", errors="replace")
            status_code = response.status
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        status_code = exc.code
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    parsed: Any
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = raw
    return {
        "prompt": prompt,
        "request": {"method": method, "url": context.target_location, "body": _redact(body)},
        "response_status": status_code,
        "response_text": _extract_response(parsed, response_path),
        "raw_response": parsed,
        "latency_ms": latency_ms,
    }


def _replace_prompt(value: Any, prompt: str) -> Any:
    if isinstance(value, str):
        return value.replace("{{prompt}}", prompt)
    if isinstance(value, list):
        return [_replace_prompt(item, prompt) for item in value]
    if isinstance(value, dict):
        return {key: _replace_prompt(item, prompt) for key, item in value.items()}
    return value


def _extract_response(value: Any, response_path: str) -> str:
    current = value
    for part in response_path.split("."):
        if not part:
            continue
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list) and part.isdigit():
            current = current[int(part)]
        else:
            break
    if isinstance(current, str):
        return current
    if current is None:
        return ""
    return json.dumps(current, sort_keys=True)


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "***redacted***" if any(token in key.lower() for token in ("key", "token", "secret", "password")) else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value
