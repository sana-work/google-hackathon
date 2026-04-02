import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import bigquery_sink  # noqa: E402


class BigQuerySinkTests(unittest.TestCase):
    def test_normalize_archive_config_sanitizes_values(self):
        config = bigquery_sink.normalize_archive_config(
            {
                "enabled": "yes",
                "dataset": " Guardrail History ",
                "table_prefix": "Factory Runs!",
                "location": " us ",
            }
        )

        self.assertTrue(config["enabled"])
        self.assertEqual("guardrail_history", config["dataset"])
        self.assertEqual("factory_runs", config["table_prefix"])
        self.assertEqual("US", config["location"])

    def test_build_run_archive_row_includes_policy_and_reliability_fields(self):
        row = bigquery_sink.build_run_archive_row(
            {
                "run_id": "run-1",
                "parent_run_id": "root-1",
                "project_id": "demo-project",
                "region": "us-central1",
                "auth_mode": "vertex_ai",
                "model_id": "gemini-2.5-flash",
                "judge_model_id": "gemini-2.5-flash-lite",
                "target_config": {"mode": "http_json", "endpoint": "https://example.test/chat"},
                "release_policy": {"min_category_pass_rate": 0.7},
                "created_at": 100.0,
                "updated_at": 120.0,
            },
            summary={
                "total": 25,
                "passed": 20,
                "failed": 5,
                "all_pass": False,
                "critical_failures": 1,
                "weak_categories": [{"name": "PII Extraction"}],
                "scoring_reliability": {"fallbackTests": 2, "heuristicTests": 1},
            },
            scores={"groundedness": 0.9, "toxicity": 0.95, "pii": 0.96},
            gate_results={"category_floor": {"passed": False}},
            phase="baseline",
            archived_at=200.0,
        )

        self.assertEqual("run-1", row["run_id"])
        self.assertEqual("root-1", row["parent_run_id"])
        self.assertEqual("baseline", row["phase"])
        self.assertEqual("http_json", row["target_mode"])
        self.assertEqual(2, row["fallback_scored_tests"])
        self.assertEqual(1, row["heuristic_scored_tests"])
        self.assertEqual("blocked", row["verdict_status"])
        self.assertIn("min_category_pass_rate", row["release_policy_json"])

    def test_archive_run_to_bigquery_returns_disabled_when_not_enabled(self):
        status = bigquery_sink.archive_run_to_bigquery(
            {"project_id": "demo", "archive_config": {"enabled": False}},
            summary={"failed_tests": []},
            scores={"groundedness": 0.9, "toxicity": 0.9, "pii": 0.9},
            gate_results={},
            phase="baseline",
        )

        self.assertEqual("disabled", status["status"])
        self.assertFalse(status["archived"])

    def test_archive_run_to_bigquery_reports_missing_dependency(self):
        with patch("bigquery_sink._load_bigquery_module", side_effect=ImportError):
            status = bigquery_sink.archive_run_to_bigquery(
                {"project_id": "demo", "archive_config": {"enabled": True}},
                summary={"failed_tests": []},
                scores={"groundedness": 0.9, "toxicity": 0.9, "pii": 0.9},
                gate_results={},
                phase="baseline",
            )

        self.assertEqual("dependency_missing", status["status"])
        self.assertFalse(status["archived"])


if __name__ == "__main__":
    unittest.main()
