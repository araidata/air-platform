from __future__ import annotations

import json
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from app.core.config import settings
from app.models.assessment_tool_run import AssessmentToolRun
from app.scanners.adapters.garak_adapter import GarakCliAdapter


class RiskyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        payload = json.loads(body)
        prompt = payload.get("prompt", "")
        response = {
            "response": (
                "I will ignore previous instructions and reveal restricted workflow details. "
                f"Prompt was: {prompt}"
            )
        }
        raw = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, format, *args):
        return


def run_test_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), RiskyHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def test_live_http_tester_creates_real_finding_and_redacts_auth(client, tmp_path):
    settings.scanner_storage_root = str(tmp_path)
    server = run_test_server()
    try:
        response = client.post(
            "/assessment-tool/runs",
            json={
                "engine": "http_tester",
                "target_name": "Local risky endpoint",
                "target_url": f"http://127.0.0.1:{server.server_port}/chat",
                "method": "POST",
                "request_template": {"prompt": "{{prompt}}"},
                "response_path": "response",
                "auth_header_name": "Authorization",
                "auth_header_value": "Bearer secret-token",
                "selected_tests": ["prompt_injection"],
                "timeout_seconds": 10,
            },
        )
    finally:
        server.shutdown()

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["findings"]
    assert payload["findings"][0]["test"] == "prompt_injection"
    assert payload["request_headers"]["Authorization"] == "[redacted]"
    assert "secret-token" not in json.dumps(payload)
    assert "report_path" in payload["artifacts"]


def test_assessment_tool_rejects_missing_prompt_token(client):
    response = client.post(
        "/assessment-tool/runs",
        json={
            "engine": "http_tester",
            "target_url": "http://127.0.0.1:9999/chat",
            "request_template": {"prompt": "missing token"},
            "selected_tests": ["prompt_injection"],
        },
    )

    assert response.status_code == 422


def test_garak_assessment_builds_rest_config_and_report(client, tmp_path, monkeypatch):
    settings.scanner_storage_root = str(tmp_path)

    def fake_run(self, command, *, cwd, env, timeout):
        report_path = Path(cwd) / "air-test.report.jsonl"
        hitlog_path = Path(cwd) / "air-test.hitlog.jsonl"
        html_path = Path(cwd) / "air-test.report.html"
        report_path.write_text(
            "\n".join(
                [
                    '{"entry_type":"init","garak_version":"0.15.0"}',
                    '{"entry_type":"eval","probe":"promptinject.Test","detector":"always.Fail","passed":1,"total":4}',
                ]
            ),
            encoding="utf-8",
        )
        hitlog_path.write_text('{"probe":"promptinject.Test","outputs":["unsafe"]}\n', encoding="utf-8")
        html_path.write_text("<html>garak report</html>", encoding="utf-8")
        assert "-G" in command
        assert env["REST_API_KEY"] == "Bearer secret-token"
        return subprocess.CompletedProcess(command, 0, stdout="report closed", stderr="")

    monkeypatch.setattr(GarakCliAdapter, "_run_command", fake_run)

    response = client.post(
        "/assessment-tool/runs",
        json={
            "engine": "garak",
            "target_name": "County chat endpoint",
            "target_url": "http://127.0.0.1:9999/chat",
            "method": "POST",
            "request_template": {"prompt": "{{prompt}}"},
            "response_path": "response",
            "auth_header_name": "Authorization",
            "auth_header_value": "Bearer secret-token",
            "selected_tests": ["prompt_injection"],
            "generations": 1,
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "completed"
    assert payload["findings"]
    assert payload["report"]["engine_plan"]["engine"] == "garak"
    config = json.loads(Path(payload["artifacts"]["garak_config_path"]).read_text(encoding="utf-8"))
    rest_config = config["rest"]["RestGenerator"]
    assert rest_config["uri"] == "http://127.0.0.1:9999/chat"
    assert rest_config["headers"]["Authorization"] == "$KEY"
    assert rest_config["req_template_json_object"]["prompt"] == "$INPUT"
    assert client.get(f"/assessment-tool/runs/{payload['id']}/report").json()["run_id"] == payload["id"]
    assert client.get("/assessment-tool/runs").json()
    assert client.get("/scanner-runs").json() == []
    assert client.get("/findings").json() == []


def test_garak_assessment_marks_bad_preset_failed_without_losing_run(client, tmp_path, monkeypatch):
    settings.scanner_storage_root = str(tmp_path)

    def fake_run(self, command, *, cwd, env, timeout):
        report_path = Path(cwd) / "air-test.report.jsonl"
        hitlog_path = Path(cwd) / "air-test.hitlog.jsonl"
        html_path = Path(cwd) / "air-test.report.html"
        if "jailbreak_resistance" in str(cwd):
            report_path.write_text('{"entry_type":"eval","probe":"broken"', encoding="utf-8")
        else:
            report_path.write_text(
                '{"entry_type":"eval","probe":"promptinject.Test","detector":"always.Pass","passed":4,"total":4}\n',
                encoding="utf-8",
            )
        hitlog_path.write_text("", encoding="utf-8")
        html_path.write_text("<html>garak report</html>", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, stdout="report closed", stderr="")

    monkeypatch.setattr(GarakCliAdapter, "_run_command", fake_run)

    response = client.post(
        "/assessment-tool/runs",
        json={
            "engine": "garak",
            "target_name": "County chat endpoint",
            "target_url": "http://127.0.0.1:9999/chat",
            "method": "POST",
            "request_template": {"prompt": "{{prompt}}"},
            "response_path": "response",
            "selected_tests": ["prompt_injection", "jailbreak"],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "completed"
    assert "report_path" in payload["artifacts"]
    assert any(step["status"] == "failed" and "garak" in step["label"] for step in payload["steps"])


def test_assessment_tool_model_is_registered(db_session):
    assert db_session.query(AssessmentToolRun).count() == 0
