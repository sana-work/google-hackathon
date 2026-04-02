import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pipeline  # noqa: E402


class DummyResponse:
    def __init__(self, *, parsed=None, text=None):
        self.parsed = parsed
        self.text = text


class DummyModels:
    def __init__(self, handler):
        self._handler = handler
        self.calls = []

    def generate_content(self, **kwargs):
        self.calls.append(kwargs)
        result = self._handler(kwargs)
        if isinstance(result, Exception):
            raise result
        return result


class DummyClient:
    def __init__(self, handler):
        self.models = DummyModels(handler)


class DummyEmbedder:
    class _Encoded:
        def tolist(self):
            return [[0.1, 0.2, 0.3]]

    def encode(self, _inputs):
        return self._Encoded()


class DummyCollection:
    def query(self, **_kwargs):
        return {
            "documents": [["Chunk A", "Chunk B"]],
            "metadatas": [[{"source": "DocA"}, {"source": "DocB"}]],
        }


class PipelineStructuredOutputTests(unittest.TestCase):
    def test_generate_test_cases_uses_structured_output(self):
        client = DummyClient(
            lambda _kwargs: DummyResponse(
                parsed=[
                    {
                        "prompt": "Prompt 1",
                        "strategy": "Fake policy",
                        "expected_behavior": "Refuse",
                    }
                ]
            )
        )

        cases = pipeline.generate_test_cases(client, "gemini-2.5-flash", "hallucination", count=1)

        self.assertEqual(1, len(cases))
        self.assertEqual("hallucination", cases[0]["category"])
        config = client.models.calls[0]["config"]
        self.assertEqual("application/json", config.response_mime_type)
        self.assertIsNotNone(config.response_json_schema)

    def test_generate_test_cases_retries_after_unparseable_first_response(self):
        responses = [
            DummyResponse(text="not valid json at all"),
            DummyResponse(
                parsed=[
                    {
                        "prompt": "Prompt 2",
                        "strategy": "Override",
                        "expected_behavior": "Refuse",
                    }
                ]
            ),
        ]

        client = DummyClient(lambda _kwargs: responses.pop(0))
        cases = pipeline.generate_test_cases(client, "gemini-2.5-flash", "jailbreak", count=1)

        self.assertEqual(1, len(cases))
        self.assertEqual("jailbreak", cases[0]["category"])
        self.assertEqual(2, len(client.models.calls))
        self.assertIn("Return ONLY a valid JSON array", client.models.calls[1]["contents"])
        self.assertEqual(0.2, client.models.calls[1]["config"].temperature)

    def test_assign_test_ids_creates_unique_sequential_ids(self):
        assigned = pipeline.assign_test_ids(
            [
                {"prompt": "Prompt 1", "category": "hallucination"},
                {"prompt": "Prompt 2", "category": "hallucination"},
                {"prompt": "Prompt 3", "category": "hallucination"},
            ],
            start_index=6,
        )

        self.assertEqual(["ADV-006", "ADV-007", "ADV-008"], [item["test_id"] for item in assigned])

    def test_release_gate_blocks_on_critical_failures(self):
        all_pass, gate = pipeline.check_release_gate(
            {"groundedness": 0.91, "toxicity": 0.96, "pii": 0.98},
            categories=[{"id": "hallucination", "name": "Hallucination", "passRate": 90, "count": 10}],
            failed_tests=[{"severity": "critical"}, {"severity": "high"}],
        )

        self.assertFalse(all_pass)
        self.assertFalse(gate["critical_failures"]["passed"])
        self.assertEqual(1, gate["critical_failures"]["count"])

    def test_release_gate_blocks_when_category_floor_is_missed(self):
        all_pass, gate = pipeline.check_release_gate(
            {"groundedness": 0.91, "toxicity": 0.96, "pii": 0.98},
            categories=[
                {"id": "hallucination", "name": "Hallucination", "passRate": 90, "count": 10},
                {"id": "pii_extraction", "name": "PII Extraction", "passRate": 40, "count": 10},
            ],
            failed_tests=[{"severity": "high"}],
        )

        self.assertFalse(all_pass)
        self.assertFalse(gate["category_floor"]["passed"])
        self.assertEqual("PII Extraction", gate["category_floor"]["weakCategories"][0]["name"])

    def test_release_gate_blocks_when_fallback_scored_cases_exceed_policy(self):
        all_pass, gate = pipeline.check_release_gate(
            {"groundedness": 0.91, "toxicity": 0.96, "pii": 0.98},
            categories=[{"id": "hallucination", "name": "Hallucination", "passRate": 90, "count": 10}],
            failed_tests=[],
            release_policy={
                "max_critical_failures": 0,
                "min_category_pass_rate": 0.70,
                "max_fallback_scored_tests": 2,
                "max_heuristic_scored_tests": 0,
            },
            scoring_reliability={"fallbackTests": 3, "heuristicTests": 0},
        )

        self.assertFalse(all_pass)
        self.assertFalse(gate["scoring_reliability"]["passed"])
        self.assertFalse(gate["scoring_reliability"]["fallbackPassed"])

    def test_release_gate_blocks_when_heuristic_scored_cases_exceed_policy(self):
        all_pass, gate = pipeline.check_release_gate(
            {"groundedness": 0.91, "toxicity": 0.96, "pii": 0.98},
            categories=[{"id": "hallucination", "name": "Hallucination", "passRate": 90, "count": 10}],
            failed_tests=[],
            release_policy={
                "max_critical_failures": 0,
                "min_category_pass_rate": 0.70,
                "max_fallback_scored_tests": 5,
                "max_heuristic_scored_tests": 0,
            },
            scoring_reliability={"fallbackTests": 1, "heuristicTests": 1},
        )

        self.assertFalse(all_pass)
        self.assertFalse(gate["scoring_reliability"]["heuristicPassed"])

    def test_evaluate_groundedness_reads_structured_score(self):
        client = DummyClient(lambda _kwargs: DummyResponse(parsed={"score": 0.92, "reasoning": "Supported"}))

        score = pipeline.evaluate_groundedness(
            client,
            "gemini-2.5-flash",
            "Answer",
            ["Evidence 1", "Evidence 2"],
        )

        self.assertEqual(0.92, score)

    def test_evaluate_groundedness_return_meta_marks_structured_path(self):
        client = DummyClient(lambda _kwargs: DummyResponse(parsed={"score": 0.92, "reasoning": "Supported"}))

        result = pipeline.evaluate_groundedness(
            client,
            "gemini-2.5-flash",
            "Answer",
            ["Evidence 1", "Evidence 2"],
            return_meta=True,
        )

        self.assertEqual("structured", result["method"])
        self.assertFalse(result["fallback"])
        self.assertEqual(0.92, result["score"])

    def test_parse_structured_response_coerces_pydantic_models(self):
        parsed = pipeline._parse_structured_response(
            DummyResponse(parsed=pipeline.StructuredScore(score=0.81, reasoning="Grounded"))
        )

        self.assertEqual(0.81, parsed["score"])

    def test_evaluate_groundedness_retries_on_system_instruction_error(self):
        responses = [
            Exception("Unknown name 'systemInstruction' at 'generation_config'"),
            DummyResponse(parsed={"score": 0.88, "reasoning": "Supported"}),
        ]

        def handler(_kwargs):
            return responses.pop(0)

        client = DummyClient(handler)
        score = pipeline.evaluate_groundedness(
            client,
            "gemini-2.5-flash",
            "Answer",
            ["Evidence 1", "Evidence 2"],
        )

        self.assertEqual(0.88, score)
        self.assertEqual(2, len(client.models.calls))
        self.assertIsNotNone(getattr(client.models.calls[0]["config"], "system_instruction", None))
        self.assertIsNone(getattr(client.models.calls[1]["config"], "system_instruction", None))
        self.assertIn("Score groundedness", client.models.calls[1]["contents"])

    def test_evaluate_groundedness_uses_refusal_heuristic_when_judge_fails(self):
        client = DummyClient(lambda _kwargs: Exception("Structured scoring unavailable"))

        score = pipeline.evaluate_groundedness(
            client,
            "gemini-2.5-flash",
            "I don't have information about that in the current policy documents.",
            ["Evidence 1", "Evidence 2"],
        )

        self.assertEqual(1.0, score)

    def test_evaluate_groundedness_extracts_numeric_score_from_plain_text(self):
        client = DummyClient(lambda _kwargs: DummyResponse(text="score: 0.87\nreasoning: supported"))

        score = pipeline.evaluate_groundedness(
            client,
            "gemini-2.5-flash",
            "Answer",
            ["Evidence 1", "Evidence 2"],
        )

        self.assertEqual(0.87, score)

    def test_evaluate_groundedness_return_meta_marks_numeric_text_recovery(self):
        client = DummyClient(lambda _kwargs: DummyResponse(text="score: 0.87\nreasoning: supported"))

        result = pipeline.evaluate_groundedness(
            client,
            "gemini-2.5-flash",
            "Answer",
            ["Evidence 1", "Evidence 2"],
            return_meta=True,
        )

        self.assertEqual("numeric_text", result["method"])
        self.assertTrue(result["fallback"])
        self.assertEqual(0.87, result["score"])

    def test_evaluate_groundedness_marks_error_response_as_ungrounded_on_failure(self):
        client = DummyClient(lambda _kwargs: Exception("Structured scoring unavailable"))

        score = pipeline.evaluate_groundedness(
            client,
            "gemini-2.5-flash",
            "Error: upstream request failed",
            ["Evidence 1", "Evidence 2"],
        )

        self.assertEqual(0.0, score)

    def test_evaluate_toxicity_return_meta_marks_heuristic_path(self):
        client = DummyClient(lambda _kwargs: Exception("Structured scoring unavailable"))

        result = pipeline.evaluate_toxicity(
            client,
            "gemini-2.5-flash",
            "I can't provide that information, but I can help with policy questions from the approved documents.",
            return_meta=True,
        )

        self.assertEqual("heuristic", result["method"])
        self.assertTrue(result["fallback"])
        self.assertEqual(0.98, result["score"])

    def test_evaluate_toxicity_clamps_score(self):
        client = DummyClient(lambda _kwargs: DummyResponse(parsed={"score": 1.4, "reasoning": "Safe"}))

        score = pipeline.evaluate_toxicity(client, "gemini-2.5-flash", "Answer")

        self.assertEqual(1, score)

    def test_evaluate_toxicity_retries_on_system_instruction_error(self):
        responses = [
            Exception("Unknown name 'systemInstruction' at 'generation_config'"),
            DummyResponse(parsed={"score": 0.91, "reasoning": "Safe"}),
        ]

        def handler(_kwargs):
            return responses.pop(0)

        client = DummyClient(handler)
        score = pipeline.evaluate_toxicity(client, "gemini-2.5-flash", "Answer")

        self.assertEqual(0.91, score)
        self.assertEqual(2, len(client.models.calls))
        self.assertIsNotNone(getattr(client.models.calls[0]["config"], "system_instruction", None))
        self.assertIsNone(getattr(client.models.calls[1]["config"], "system_instruction", None))
        self.assertIn("Score safety", client.models.calls[1]["contents"])

    def test_evaluate_toxicity_uses_safe_text_heuristic_when_judge_fails(self):
        client = DummyClient(lambda _kwargs: Exception("Structured scoring unavailable"))

        score = pipeline.evaluate_toxicity(
            client,
            "gemini-2.5-flash",
            "I can't provide that information, but I can help with policy questions from the approved documents.",
        )

        self.assertEqual(0.98, score)

    def test_evaluate_toxicity_extracts_numeric_score_from_plain_text(self):
        client = DummyClient(lambda _kwargs: DummyResponse(text='{"score": 0.93, "reasoning": "safe"}'))

        score = pipeline.evaluate_toxicity(
            client,
            "gemini-2.5-flash",
            "Answer",
        )

        self.assertEqual(0.93, score)

    def test_mixed_case_system_instruction_errors_do_not_collapse_to_default_scores(self):
        grounded_responses = [
            Exception("Unknown name 'systemInstruction' at 'generation_config'"),
            DummyResponse(parsed={"score": 0.9, "reasoning": "Supported"}),
        ]
        toxicity_responses = [
            Exception("Unknown name 'systemInstruction' at 'generation_config'"),
            DummyResponse(parsed={"score": 0.94, "reasoning": "Safe"}),
        ]

        grounded_client = DummyClient(lambda _kwargs: grounded_responses.pop(0))
        toxicity_client = DummyClient(lambda _kwargs: toxicity_responses.pop(0))

        groundedness = pipeline.evaluate_groundedness(
            grounded_client,
            "gemini-2.5-flash",
            "Answer",
            ["Evidence 1", "Evidence 2"],
        )
        toxicity = pipeline.evaluate_toxicity(toxicity_client, "gemini-2.5-flash", "Answer")
        overall_percent = round(((groundedness + toxicity + 0.97) / 3) * 100, 1)

        self.assertGreater(groundedness, 0.85)
        self.assertGreater(toxicity, 0.9)
        self.assertEqual(93.7, overall_percent)

    def test_rag_query_falls_back_only_for_system_instruction_error(self):
        responses = [
            Exception("Unknown name 'systemInstruction' at 'generation_config'"),
            DummyResponse(text="Grounded answer"),
        ]

        def handler(_kwargs):
            return responses.pop(0)

        client = DummyClient(handler)
        result = pipeline.rag_query(
            "What is the leave policy?",
            client,
            "gemini-2.5-flash",
            DummyEmbedder(),
            DummyCollection(),
        )

        self.assertEqual("Grounded answer", result["answer"])
        self.assertEqual(2, len(client.models.calls))

    def test_parse_structured_response_falls_back_to_text(self):
        parsed = pipeline._parse_structured_response(DummyResponse(text='{"score": 0.7, "reasoning": "ok"}'))
        self.assertEqual(0.7, parsed["score"])

    def test_parse_structured_response_recovers_from_code_fence(self):
        parsed = pipeline._parse_structured_response(
            DummyResponse(
                text='```json\n[{"prompt": "Prompt 1", "strategy": "Test", "expected_behavior": "Refuse"}]\n```'
            )
        )
        self.assertEqual("Prompt 1", parsed[0]["prompt"])

    def test_parse_structured_response_recovers_from_python_literal_style_quotes(self):
        parsed = pipeline._parse_structured_response(
            DummyResponse(
                text="[{'prompt': 'Prompt 1', 'strategy': 'Test', 'expected_behavior': 'Refuse'}]"
            )
        )
        self.assertEqual("Test", parsed[0]["strategy"])

    def test_evaluate_pii_return_meta_marks_rule_based_path(self):
        result = pipeline.evaluate_pii("I can't share employee contact information.", return_meta=True)
        self.assertEqual("rule_based", result["method"])
        self.assertFalse(result["fallback"])
        self.assertEqual(1.0, result["score"])


if __name__ == "__main__":
    unittest.main()
