#!/usr/bin/env python3
"""Unified test runner for the GenAI Guardrail Factory project.

Offline mode runs:
- Python compile checks for server.py and pipeline.py
- Notebook code-cell compile checks
- unittest discovery in tests/

Live mode additionally runs:
- FastAPI startup smoke test
- /api/configure
- /api/initialize
- /api/generate-tests
- /api/evaluate

`--all` includes live mode plus remediation.
"""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
NOTEBOOKS = [
    BASE_DIR / "01_Setup_and_RAG_App.ipynb",
    BASE_DIR / "02_Adversarial_Test_Generator.ipynb",
    BASE_DIR / "03_Evaluation_Pipeline.ipynb",
    BASE_DIR / "04_Auto_Remediation.ipynb",
]
PYTHON_FILES = [
    BASE_DIR / "server.py",
    BASE_DIR / "pipeline.py",
    BASE_DIR / "run_store.py",
    BASE_DIR / "target_apps.py",
]
DEFAULT_REPORT_PATH = BASE_DIR / "test_report.json"
DEFAULT_SERVER_LOG_PATH = BASE_DIR / "test_server.log"
DEFAULT_BASE_URL = "http://127.0.0.1:8000"


class StepFailed(RuntimeError):
    """Raised when a test step fails."""


def log(message: str) -> None:
    print(message, flush=True)


def print_step(title: str) -> None:
    log(f"\n=== {title} ===")


def tail_text(path: Path, *, max_lines: int = 60) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    return "\n".join(lines[-max_lines:])


def add_result(report: dict, *, name: str, ok: bool, message: str, output: str = "", duration: float | None = None) -> None:
    report["steps"].append(
        {
            "name": name,
            "ok": ok,
            "message": message,
            "output": output,
            "duration_seconds": None if duration is None else round(duration, 3),
        }
    )


def write_report(report: dict, report_path: Path) -> None:
    report["finished_at_epoch"] = int(time.time())
    report["success"] = all(step["ok"] for step in report["steps"])
    report_path.write_text(json.dumps(report, indent=2))


def run_command(args: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def run_compile_checks(report: dict) -> None:
    start = time.time()
    print_step("Python Compile Checks")
    try:
        for path in PYTHON_FILES:
            py_compile.compile(str(path), doraise=True)
        message = "server.py and pipeline.py compiled successfully."
        log(message)
        add_result(report, name="py_compile", ok=True, message=message, duration=time.time() - start)
    except Exception as exc:
        message = f"Compile check failed: {exc}"
        log(message)
        add_result(
            report,
            name="py_compile",
            ok=False,
            message=message,
            output=traceback.format_exc(),
            duration=time.time() - start,
        )


def run_notebook_checks(report: dict) -> None:
    start = time.time()
    print_step("Notebook Checks")
    try:
        for notebook in NOTEBOOKS:
            data = json.loads(notebook.read_text())
            source = "\n".join(
                "".join(cell.get("source", []))
                for cell in data.get("cells", [])
                if cell.get("cell_type") == "code"
            )
            if "import vertexai" in source or "vertexai.generative_models" in source:
                raise StepFailed(f"Deprecated Vertex AI SDK usage found in {notebook.name}")

            chunks = []
            for cell in data.get("cells", []):
                if cell.get("cell_type") != "code":
                    continue
                lines = []
                for line in cell.get("source", []):
                    stripped = line.lstrip()
                    if stripped.startswith("!") or stripped.startswith("%"):
                        continue
                    lines.append(line)
                source_chunk = "".join(lines).strip()
                if source_chunk:
                    chunks.append(source_chunk)

            compile("\n\n".join(chunks), f"{notebook.name}", "exec")

        message = "All notebook code cells compiled after stripping magics, and no deprecated vertexai SDK usage remains."
        log(message)
        add_result(report, name="notebooks", ok=True, message=message, duration=time.time() - start)
    except Exception as exc:
        message = f"Notebook checks failed: {exc}"
        log(message)
        add_result(
            report,
            name="notebooks",
            ok=False,
            message=message,
            output=traceback.format_exc(),
            duration=time.time() - start,
        )


def run_unittest_suite(report: dict) -> None:
    start = time.time()
    print_step("Unit Tests")
    proc = run_command(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=BASE_DIR,
    )
    ok = proc.returncode == 0
    message = "unittest suite passed." if ok else f"unittest suite failed with exit code {proc.returncode}."
    log(message)
    log(proc.stdout)
    if proc.stderr:
        log(proc.stderr)
    add_result(
        report,
        name="unittest",
        ok=ok,
        message=message,
        output=(proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else ""),
        duration=time.time() - start,
    )


def http_json(method: str, url: str, payload: dict | None = None, timeout: float = 30.0, headers: dict | None = None) -> dict:
    body = None
    request_headers = {"Accept": "application/json"}
    if headers:
        request_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        request_headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {}


def wait_for_server(base_url: str, *, timeout_seconds: float, headers: dict | None = None) -> None:
    deadline = time.time() + timeout_seconds
    url = f"{base_url}/api/status"
    last_error = None
    last_report = 0.0
    while time.time() < deadline:
        try:
            http_json("GET", url, timeout=5.0, headers=headers)
            return
        except Exception as exc:
            last_error = exc
            now = time.time()
            if now - last_report >= 5:
                remaining = max(0, int(deadline - now))
                log(f"[live] Waiting for FastAPI server at {base_url} ... {remaining}s remaining")
                last_report = now
            time.sleep(1)
    raise StepFailed(f"Server did not become ready within {timeout_seconds:.0f}s: {last_error}")


def poll_status(base_url: str, expected_stage: int, *, timeout_seconds: float, label: str, headers: dict | None = None) -> dict:
    deadline = time.time() + timeout_seconds
    status_url = f"{base_url}/api/status"
    last_payload = {}
    last_message = None
    last_report = 0.0
    while time.time() < deadline:
        last_payload = http_json("GET", status_url, timeout=10.0, headers=headers)
        current_status = last_payload.get("status")
        current_stage = last_payload.get("active_stage", last_payload.get("stage", 0))
        progress = last_payload.get("progress", 0)
        progress_text = last_payload.get("progress_text", "")
        message = f"[{label}] stage={current_stage} status={current_status} progress={progress}% text={progress_text}"
        now = time.time()
        if message != last_message or now - last_report >= 10:
            log(message)
            last_message = message
            last_report = now
        if current_status == "error":
            raise StepFailed(last_payload.get("error") or f"Stage {expected_stage} returned error status.")
        if current_status == "done" and current_stage >= expected_stage:
            return last_payload
        time.sleep(2)
    raise StepFailed(
        f"Timed out waiting for stage {expected_stage}. Last status payload: {json.dumps(last_payload, indent=2)}"
    )


def get_api_key(cli_value: str | None) -> str | None:
    if cli_value:
        return cli_value.strip()
    for env_name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        value = os.environ.get(env_name, "").strip()
        if value:
            return value
    return None


def get_admin_headers() -> dict:
    token = os.environ.get("GUARDRAIL_ADMIN_TOKEN", "").strip()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def run_live_flow(
    report: dict,
    *,
    base_url: str,
    project_id: str,
    region: str,
    model_id: str,
    api_key: str | None,
    server_timeout: float,
    stage_timeout: float,
    include_remediation: bool,
    report_path: Path,
    server_log_path: Path,
) -> None:
    print_step("Live FastAPI Smoke Test")
    start = time.time()
    server_log = server_log_path.open("w", encoding="utf-8")
    process = None
    auth_headers = get_admin_headers()

    try:
        log(f"[live] Starting FastAPI server. Log: {server_log_path}")
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            cwd=str(BASE_DIR),
            stdout=server_log,
            stderr=subprocess.STDOUT,
            text=True,
        )

        wait_for_server(base_url, timeout_seconds=server_timeout, headers=auth_headers)
        log("[live] FastAPI server is responding.")

        root_response = urllib.request.urlopen(f"{base_url}/", timeout=10.0).read().decode("utf-8")
        if "GenAI Guardrail Factory" not in root_response:
            raise StepFailed("Dashboard root endpoint did not return expected HTML content.")
        log("[live] Dashboard root endpoint responded.")

        config_payload = {
            "project_id": project_id,
            "region": region,
            "model_id": model_id,
        }
        if api_key:
            config_payload["api_key"] = api_key

        config_payload["judge_model_id"] = "gemini-2.5-flash-lite"
        config_payload["target_config"] = {"mode": "local_rag"}
        http_json("POST", f"{base_url}/api/configure", config_payload, timeout=15.0, headers=auth_headers)
        log(f"[live] Configuration sent: project_id={project_id}, region={region}, model_id={model_id}")

        log("[live] Starting initialization...")
        http_json("POST", f"{base_url}/api/initialize", timeout=15.0, headers=auth_headers)
        init_status = poll_status(base_url, 1, timeout_seconds=stage_timeout, label="initialize", headers=auth_headers)
        if init_status.get("error"):
            raise StepFailed(f"Initialization error: {init_status['error']}")
        log("[live] Initialization completed.")

        log("[live] Starting adversarial test generation...")
        http_json("POST", f"{base_url}/api/generate-tests", timeout=15.0, headers=auth_headers)
        test_status = poll_status(base_url, 2, timeout_seconds=stage_timeout, label="generate-tests", headers=auth_headers)
        if int(test_status.get("test_cases_count", 0)) <= 0:
            raise StepFailed("Test generation finished but no test cases were created.")
        log(f"[live] Test generation completed with {test_status.get('test_cases_count', 0)} tests.")

        log("[live] Starting evaluation...")
        http_json("POST", f"{base_url}/api/evaluate", timeout=15.0, headers=auth_headers)
        eval_status = poll_status(base_url, 3, timeout_seconds=stage_timeout, label="evaluate", headers=auth_headers)
        results_payload = http_json("GET", f"{base_url}/api/results", timeout=20.0, headers=auth_headers)

        if not results_payload.get("ready"):
            raise StepFailed("/api/results returned ready=false after evaluation.")
        if int(results_payload.get("totalTests", 0)) <= 0:
            raise StepFailed("Evaluation completed but totalTests was 0.")

        scores = results_payload.get("scores", {})
        for key in ("groundedness", "toxicity", "pii"):
            if key not in scores:
                raise StepFailed(f"Missing '{key}' in evaluation scores.")

        categories = results_payload.get("categories", [])
        if len(categories) != 5:
            raise StepFailed(f"Expected 5 category buckets, got {len(categories)}.")
        log(
            "[live] Evaluation completed. "
            f"totalTests={results_payload.get('totalTests')} passed={results_payload.get('passed')} failed={results_payload.get('failed')}"
        )
        log(f"[live] Scores: {json.dumps(scores)}")

        remediation_summary = "skipped"
        if include_remediation:
            log("[live] Starting remediation...")
            http_json("POST", f"{base_url}/api/remediate", timeout=15.0, headers=auth_headers)
            poll_status(base_url, 4, timeout_seconds=stage_timeout, label="remediate", headers=auth_headers)
            rem_results = http_json("GET", f"{base_url}/api/results", timeout=20.0, headers=auth_headers)
            if not rem_results.get("beforeScores") or not rem_results.get("afterScores"):
                raise StepFailed("Remediation finished but beforeScores/afterScores were missing.")
            if not rem_results.get("improvedPrompt"):
                raise StepFailed("Remediation finished but improvedPrompt was missing.")
            remediation_summary = "completed"
            log("[live] Remediation completed.")

        message = (
            f"Live flow passed. totalTests={results_payload.get('totalTests')}, "
            f"model={model_id}, remediation={remediation_summary}."
        )
        log(message)
        add_result(
            report,
            name="live_fastapi_flow",
            ok=True,
            message=message,
            output=json.dumps(
                {
                    "init_status": init_status,
                    "eval_status": eval_status,
                    "results_summary": {
                        "totalTests": results_payload.get("totalTests"),
                        "passed": results_payload.get("passed"),
                        "failed": results_payload.get("failed"),
                        "scores": results_payload.get("scores"),
                    },
                },
                indent=2,
            ),
            duration=time.time() - start,
        )
    except Exception as exc:
        server_log.flush()
        message = f"Live flow failed: {exc}"
        log(message)
        log(f"[live] See server log: {server_log_path}")
        tail = tail_text(server_log_path)
        if tail:
            log("[live] Last server log lines:")
            log(tail)
        add_result(
            report,
            name="live_fastapi_flow",
            ok=False,
            message=message,
            output=traceback.format_exc() + ("\n\nServer log tail:\n" + tail if tail else ""),
            duration=time.time() - start,
        )
    finally:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        server_log.close()
        write_report(report, report_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run offline and optional live tests for the GenAI Guardrail Factory project.")
    parser.add_argument("--live", action="store_true", help="Run the live FastAPI + Gemini smoke flow after offline checks.")
    parser.add_argument("--remediate", action="store_true", help="Include remediation stage in live mode.")
    parser.add_argument("--all", action="store_true", help="Run live mode plus remediation.")
    parser.add_argument("--project-id", default="tcs-1770741136478", help="Project id to send to /api/configure.")
    parser.add_argument("--region", default="us-central1", help="Region to send to /api/configure.")
    parser.add_argument("--model-id", default="gemini-2.5-flash", help="Model id to send to /api/configure.")
    parser.add_argument("--api-key", default=None, help="Optional Gemini Developer API key. If omitted, env vars are used.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Base URL for live smoke requests.")
    parser.add_argument("--server-timeout", type=float, default=60.0, help="Seconds to wait for the FastAPI server to start.")
    parser.add_argument("--stage-timeout", type=float, default=900.0, help="Seconds to wait for each pipeline stage.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT_PATH), help="Where to write the JSON test report.")
    parser.add_argument("--server-log", default=str(DEFAULT_SERVER_LOG_PATH), help="Where to write live server logs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_live = args.live or args.all
    include_remediation = args.remediate or args.all
    report_path = Path(args.report).resolve()
    server_log_path = Path(args.server_log).resolve()

    report = {
        "base_dir": str(BASE_DIR),
        "python_executable": sys.executable,
        "argv": sys.argv[1:],
        "started_at_epoch": int(time.time()),
        "steps": [],
    }

    run_compile_checks(report)
    write_report(report, report_path)

    run_notebook_checks(report)
    write_report(report, report_path)

    run_unittest_suite(report)
    write_report(report, report_path)

    if run_live:
        api_key = get_api_key(args.api_key)
        run_live_flow(
            report,
            base_url=args.base_url.rstrip("/"),
            project_id=args.project_id,
            region=args.region,
            model_id=args.model_id,
            api_key=api_key,
            server_timeout=args.server_timeout,
            stage_timeout=args.stage_timeout,
            include_remediation=include_remediation,
            report_path=report_path,
            server_log_path=server_log_path,
        )
    else:
        log("\nLive smoke flow was skipped. Use --live or --all to exercise FastAPI and Gemini.")

    write_report(report, report_path)
    failed_steps = [step for step in report["steps"] if not step["ok"]]

    print_step("Summary")
    log(f"Report written to: {report_path}")
    if server_log_path.exists() and run_live:
        log(f"Server log written to: {server_log_path}")

    if failed_steps:
        log(f"FAILED: {len(failed_steps)} step(s) failed.")
        for step in failed_steps:
            log(f"- {step['name']}: {step['message']}")
        return 1

    log("SUCCESS: all requested test steps passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
