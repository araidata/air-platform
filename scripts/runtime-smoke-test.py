from __future__ import annotations

import argparse
import json
import subprocess
import sys
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen


def fetch_json(url: str) -> Any:
    with urlopen(url, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str) -> str:
    with urlopen(url, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"{url} returned HTTP {response.status}")
        return response.read().decode("utf-8", errors="replace")


def check_list(url: str, label: str, *, require_records: bool = True) -> int:
    data = fetch_json(url)
    if not isinstance(data, list):
        raise RuntimeError(f"{label} did not return a JSON list")
    if require_records and not data:
        raise RuntimeError(f"{label} returned no seeded records")
    print(f"ok - {label}: {len(data)} records")
    return len(data)


def run_docker_check(command: list[str], label: str) -> None:
    result = subprocess.run(command, check=False, text=True, capture_output=True)
    if result.returncode != 0:
        output = result.stdout.strip() or result.stderr.strip()
        raise RuntimeError(f"{label} failed: {output}")
    print(f"ok - {label}: {(result.stdout.strip() or 'passed')}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Runtime smoke test for Docker Compose.")
    parser.add_argument("--frontend-url", default="http://localhost:3000")
    parser.add_argument("--backend-url", default="http://localhost:8000")
    parser.add_argument(
        "--skip-docker",
        action="store_true",
        help="Skip docker compose exec checks when testing externally.",
    )
    args = parser.parse_args()

    try:
        health = fetch_json(f"{args.backend_url}/health")
        if health != {"status": "ok"}:
            raise RuntimeError(f"Unexpected backend health response: {health}")
        print("ok - backend health")

        db_health = fetch_json(f"{args.backend_url}/health/db")
        if db_health.get("status") != "ok" or db_health.get("database") != "ok":
            raise RuntimeError(f"Unexpected DB health response: {db_health}")
        print("ok - database health")

        check_list(f"{args.backend_url}/systems", "systems endpoint")
        check_list(f"{args.backend_url}/findings", "findings endpoint", require_records=False)
        check_list(f"{args.backend_url}/evidence", "evidence endpoint", require_records=False)
        check_list(f"{args.backend_url}/assessments", "assessments endpoint", require_records=False)
        check_list(f"{args.backend_url}/scanner-runs", "scanner runs endpoint", require_records=False)

        html = fetch_text(args.frontend_url)
        if "Executive Dashboard" not in html:
            raise RuntimeError("Frontend did not render the dashboard route")
        print("ok - frontend dashboard")

        proxied_health = fetch_json(f"{args.frontend_url}/api/backend/health")
        if proxied_health != {"status": "ok"}:
            raise RuntimeError(f"Unexpected frontend proxy health response: {proxied_health}")
        print("ok - frontend/backend proxy")

        if not args.skip_docker:
            run_docker_check(
                ["docker", "compose", "exec", "-T", "backend", "alembic", "current"],
                "alembic current",
            )

        print("runtime smoke test passed")
        return 0
    except (RuntimeError, URLError, TimeoutError) as exc:
        print(f"smoke test failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
