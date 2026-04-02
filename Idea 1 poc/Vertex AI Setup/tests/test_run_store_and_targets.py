import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from run_store import RunStore  # noqa: E402
from target_apps import execute_target, normalize_target_config  # noqa: E402


class RunStoreTests(unittest.TestCase):
    def test_run_store_persists_default_config_and_runs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = RunStore(Path(tmpdir) / "guardrail.db")
            defaults = {"project_id": "demo", "tests_per_cat": 5}
            self.assertEqual(defaults, store.get_default_config(defaults))

            stored_config = {"project_id": "prod", "tests_per_cat": 10}
            store.save_default_config(stored_config)
            self.assertEqual(stored_config, store.get_default_config(defaults))

            run = {
                "run_id": "run-123",
                "status": "idle",
                "stage": 0,
                "active_stage": 0,
                "progress": 0,
                "progress_text": "",
            }
            created = store.create_run(run)
            self.assertEqual("run-123", created["run_id"])
            self.assertEqual("run-123", store.get_current_run_id())

            updated = store.update_run("run-123", {"status": "done", "stage": 3, "progress": 100})
            self.assertEqual("done", updated["status"])
            self.assertEqual(3, updated["stage"])
            self.assertEqual(100, updated["progress"])

    def test_create_run_populates_missing_created_at_when_value_is_none(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = RunStore(Path(tmpdir) / "guardrail.db")
            created = store.create_run(
                {
                    "run_id": "run-none-created-at",
                    "status": "idle",
                    "stage": 0,
                    "active_stage": 0,
                    "created_at": None,
                }
            )

            self.assertIsInstance(created["created_at"], float)
            self.assertIsInstance(created["updated_at"], float)
            persisted = store.get_run("run-none-created-at")
            self.assertIsInstance(persisted["created_at"], float)


class TargetAdapterTests(unittest.TestCase):
    def test_normalize_target_config_fills_defaults(self):
        config = normalize_target_config({"mode": "http_json", "endpoint": " https://example.test/api "})
        self.assertEqual("http_json", config["mode"])
        self.assertEqual("https://example.test/api", config["endpoint"])
        self.assertEqual("prompt", config["prompt_field"])
        self.assertEqual("response", config["response_field"])

    def test_execute_target_uses_runtime_local_executor_for_local_rag(self):
        calls = []

        def local_executor(prompt, client, model_id, embedder, collection, system_prompt=None):
            calls.append(
                {
                    "prompt": prompt,
                    "client": client,
                    "model_id": model_id,
                    "embedder": embedder,
                    "collection": collection,
                    "system_prompt": system_prompt,
                }
            )
            return {
                "question": prompt,
                "answer": "Stubbed answer",
                "sources": ["DocA"],
                "context_chunks": ["Chunk A"],
            }

        runtime_context = {
            "client": object(),
            "embedder": object(),
            "collection": object(),
            "local_executor": local_executor,
        }

        result = execute_target(
            "What is the policy?",
            runtime_context,
            model_id="gemini-2.5-flash",
            target_config={"mode": "local_rag"},
            system_prompt="Use evidence only",
        )

        self.assertEqual("Stubbed answer", result["answer"])
        self.assertEqual("Use evidence only", calls[0]["system_prompt"])


if __name__ == "__main__":
    unittest.main()
