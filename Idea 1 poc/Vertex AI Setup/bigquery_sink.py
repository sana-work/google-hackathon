"""Optional BigQuery archive sink for evaluation and remediation runs."""

from __future__ import annotations

import json
import re
import time
from copy import deepcopy


DEFAULT_ARCHIVE_CONFIG = {
    "provider": "bigquery",
    "enabled": False,
    "dataset": "guardrail_factory",
    "table_prefix": "guardrail",
    "location": "US",
}


def _normalize_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "on", "enabled"}:
        return True
    if text in {"0", "false", "no", "off", "disabled"}:
        return False
    return default


def _normalize_identifier(value, fallback):
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or fallback


def normalize_archive_config(config: dict | None = None) -> dict:
    source = deepcopy(DEFAULT_ARCHIVE_CONFIG)
    if config:
        source.update({k: v for k, v in config.items() if v is not None})
    return {
        "provider": "bigquery",
        "enabled": _normalize_bool(source.get("enabled"), DEFAULT_ARCHIVE_CONFIG["enabled"]),
        "dataset": _normalize_identifier(source.get("dataset"), DEFAULT_ARCHIVE_CONFIG["dataset"]),
        "table_prefix": _normalize_identifier(source.get("table_prefix"), DEFAULT_ARCHIVE_CONFIG["table_prefix"]),
        "location": str(source.get("location") or DEFAULT_ARCHIVE_CONFIG["location"]).strip().upper() or DEFAULT_ARCHIVE_CONFIG["location"],
    }


def _load_bigquery_module():
    from google.cloud import bigquery

    return bigquery


def build_run_archive_row(run: dict, *, summary: dict, scores: dict, gate_results: dict, phase: str, archived_at: float | None = None) -> dict:
    archived_at = archived_at or time.time()
    return {
        "run_id": run.get("run_id"),
        "parent_run_id": run.get("parent_run_id"),
        "phase": phase,
        "archived_at_epoch": float(archived_at),
        "run_created_at_epoch": float(run.get("created_at") or archived_at),
        "run_updated_at_epoch": float(run.get("updated_at") or archived_at),
        "project_id": run.get("project_id"),
        "region": run.get("region"),
        "auth_mode": run.get("auth_mode"),
        "run_mode": "demo" if run.get("demo_mode") else "live",
        "model_id": run.get("model_id"),
        "judge_model_id": run.get("judge_model_id") or run.get("model_id"),
        "target_mode": ((run.get("target_config") or {}).get("mode") or "local_rag"),
        "target_endpoint": ((run.get("target_config") or {}).get("endpoint") or ""),
        "total_tests": int(summary.get("total") or 0),
        "passed_tests": int(summary.get("passed") or 0),
        "failed_tests": int(summary.get("failed") or 0),
        "all_pass": bool(summary.get("all_pass")),
        "groundedness_score": float(scores.get("groundedness") or 0.0),
        "toxicity_score": float(scores.get("toxicity") or 0.0),
        "pii_score": float(scores.get("pii") or 0.0),
        "critical_failures": int(summary.get("critical_failures") or 0),
        "weak_category_count": int(len(summary.get("weak_categories") or [])),
        "fallback_scored_tests": int(((summary.get("scoring_reliability") or {}).get("fallbackTests")) or 0),
        "heuristic_scored_tests": int(((summary.get("scoring_reliability") or {}).get("heuristicTests")) or 0),
        "verdict_status": "approved" if summary.get("all_pass") else "blocked",
        "release_policy_json": json.dumps(run.get("release_policy") or {}),
        "gate_results_json": json.dumps(gate_results or {}),
    }


def build_failed_case_rows(run: dict, *, failed_tests: list[dict], phase: str, archived_at: float | None = None) -> list[dict]:
    archived_at = archived_at or time.time()
    rows = []
    for test in failed_tests or []:
        rows.append(
            {
                "run_id": run.get("run_id"),
                "phase": phase,
                "archived_at_epoch": float(archived_at),
                "test_id": test.get("id"),
                "category": test.get("cat"),
                "prompt": test.get("prompt"),
                "groundedness_score": float(test.get("ground") or 0.0),
                "toxicity_score": float(test.get("safety") or 0.0),
                "pii_score": float(test.get("pii") or 0.0),
                "severity": test.get("severity"),
                "judge_mode": test.get("judgeMode") or "unknown",
            }
        )
    return rows


def _ensure_tables(client, bigquery, *, project_id: str, archive_config: dict) -> tuple[str, str]:
    dataset_id = f"{project_id}.{archive_config['dataset']}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = archive_config["location"]
    client.create_dataset(dataset, exists_ok=True)

    runs_table_id = f"{dataset_id}.{archive_config['table_prefix']}_runs"
    failed_table_id = f"{dataset_id}.{archive_config['table_prefix']}_failed_cases"

    runs_table = bigquery.Table(
        runs_table_id,
        schema=[
            bigquery.SchemaField("run_id", "STRING"),
            bigquery.SchemaField("parent_run_id", "STRING"),
            bigquery.SchemaField("phase", "STRING"),
            bigquery.SchemaField("archived_at_epoch", "FLOAT"),
            bigquery.SchemaField("run_created_at_epoch", "FLOAT"),
            bigquery.SchemaField("run_updated_at_epoch", "FLOAT"),
            bigquery.SchemaField("project_id", "STRING"),
            bigquery.SchemaField("region", "STRING"),
            bigquery.SchemaField("auth_mode", "STRING"),
            bigquery.SchemaField("run_mode", "STRING"),
            bigquery.SchemaField("model_id", "STRING"),
            bigquery.SchemaField("judge_model_id", "STRING"),
            bigquery.SchemaField("target_mode", "STRING"),
            bigquery.SchemaField("target_endpoint", "STRING"),
            bigquery.SchemaField("total_tests", "INTEGER"),
            bigquery.SchemaField("passed_tests", "INTEGER"),
            bigquery.SchemaField("failed_tests", "INTEGER"),
            bigquery.SchemaField("all_pass", "BOOLEAN"),
            bigquery.SchemaField("groundedness_score", "FLOAT"),
            bigquery.SchemaField("toxicity_score", "FLOAT"),
            bigquery.SchemaField("pii_score", "FLOAT"),
            bigquery.SchemaField("critical_failures", "INTEGER"),
            bigquery.SchemaField("weak_category_count", "INTEGER"),
            bigquery.SchemaField("fallback_scored_tests", "INTEGER"),
            bigquery.SchemaField("heuristic_scored_tests", "INTEGER"),
            bigquery.SchemaField("verdict_status", "STRING"),
            bigquery.SchemaField("release_policy_json", "STRING"),
            bigquery.SchemaField("gate_results_json", "STRING"),
        ],
    )
    failed_table = bigquery.Table(
        failed_table_id,
        schema=[
            bigquery.SchemaField("run_id", "STRING"),
            bigquery.SchemaField("phase", "STRING"),
            bigquery.SchemaField("archived_at_epoch", "FLOAT"),
            bigquery.SchemaField("test_id", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("prompt", "STRING"),
            bigquery.SchemaField("groundedness_score", "FLOAT"),
            bigquery.SchemaField("toxicity_score", "FLOAT"),
            bigquery.SchemaField("pii_score", "FLOAT"),
            bigquery.SchemaField("severity", "STRING"),
            bigquery.SchemaField("judge_mode", "STRING"),
        ],
    )
    client.create_table(runs_table, exists_ok=True)
    client.create_table(failed_table, exists_ok=True)
    return runs_table_id, failed_table_id


def archive_run_to_bigquery(run: dict, *, summary: dict, scores: dict, gate_results: dict, phase: str) -> dict:
    archive_config = normalize_archive_config(run.get("archive_config"))
    status = {
        "provider": "bigquery",
        "enabled": archive_config["enabled"],
        "archived": False,
        "status": "disabled",
        "message": "BigQuery archiving is disabled.",
        "dataset": archive_config["dataset"],
        "tablePrefix": archive_config["table_prefix"],
        "location": archive_config["location"],
        "phase": phase,
        "rowsWritten": 0,
    }
    if not archive_config["enabled"]:
        return status

    try:
        bigquery = _load_bigquery_module()
    except ImportError:
        status.update(
            {
                "status": "dependency_missing",
                "message": "google-cloud-bigquery is not installed. Install it and enable the BigQuery API to archive runs.",
            }
        )
        return status

    try:
        client = bigquery.Client(project=run.get("project_id"))
        runs_table_id, failed_table_id = _ensure_tables(
            client,
            bigquery,
            project_id=run.get("project_id"),
            archive_config=archive_config,
        )

        archived_at = time.time()
        run_summary = {
            **summary,
            "all_pass": summary.get("all_pass", False),
        }
        run_row = build_run_archive_row(
            run,
            summary=run_summary,
            scores=scores,
            gate_results=gate_results,
            phase=phase,
            archived_at=archived_at,
        )
        failed_rows = build_failed_case_rows(
            run,
            failed_tests=summary.get("failed_tests") or [],
            phase=phase,
            archived_at=archived_at,
        )

        run_errors = client.insert_rows_json(runs_table_id, [run_row])
        if run_errors:
            status.update(
                {
                    "status": "error",
                    "message": f"Failed to archive run summary to BigQuery: {run_errors}",
                    "runsTable": runs_table_id,
                    "failedCasesTable": failed_table_id,
                }
            )
            return status

        if failed_rows:
            failed_errors = client.insert_rows_json(failed_table_id, failed_rows)
            if failed_errors:
                status.update(
                    {
                        "status": "partial",
                        "message": f"Run summary archived, but failed-case rows hit BigQuery errors: {failed_errors}",
                        "runsTable": runs_table_id,
                        "failedCasesTable": failed_table_id,
                        "rowsWritten": 1,
                    }
                )
                return status

        status.update(
            {
                "archived": True,
                "status": "archived",
                "message": f"Archived to BigQuery dataset {archive_config['dataset']}.",
                "runsTable": runs_table_id,
                "failedCasesTable": failed_table_id,
                "rowsWritten": 1 + len(failed_rows),
            }
        )
        return status
    except Exception as exc:  # pragma: no cover - exercised via live integration
        status.update(
            {
                "status": "error",
                "message": f"BigQuery archive failed: {str(exc)[:220]}",
            }
        )
        return status
