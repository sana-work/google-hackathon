"""Pluggable application-under-test adapters."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from pipeline import rag_query, retrieve_context


def normalize_target_config(config: dict | None) -> dict:
    config = dict(config or {})
    mode = config.get("mode") or "local_rag"
    return {
        "mode": mode,
        "endpoint": (config.get("endpoint") or "").strip(),
        "prompt_field": (config.get("prompt_field") or "prompt").strip() or "prompt",
        "response_field": (config.get("response_field") or "response").strip() or "response",
        "include_retrieval_context": bool(config.get("include_retrieval_context", True)),
    }


def _local_rag(prompt, runtime_context, model_id, system_prompt=None):
    executor = runtime_context.get("local_executor") or rag_query
    return executor(
        prompt,
        runtime_context["client"],
        model_id,
        runtime_context["embedder"],
        runtime_context["collection"],
        system_prompt=system_prompt,
    )


def _http_json(prompt, runtime_context, target_config, system_prompt=None):
    if not target_config.get("endpoint"):
        raise ValueError("target_endpoint is required when target_mode is http_json.")

    retrieval = retrieve_context(
        prompt,
        runtime_context["embedder"],
        runtime_context["collection"],
        top_k=5,
    )
    payload = {
        target_config["prompt_field"]: prompt,
        "system_prompt": system_prompt,
    }
    if target_config.get("include_retrieval_context", True):
        payload["retrieval_context"] = retrieval["context_text"]
        payload["retrieval_sources"] = retrieval["sources"]

    request = urllib.request.Request(
        target_config["endpoint"],
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=45.0) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"External target returned HTTP {exc.code}: {body[:240]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"External target request failed: {exc.reason}") from exc

    try:
        parsed = json.loads(raw or "{}")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"External target returned invalid JSON: {raw[:240]}") from exc

    answer = parsed.get(target_config["response_field"])
    if answer is None:
        answer = parsed.get("answer") or parsed.get("response")
    if answer is None:
        raise RuntimeError(
            f"External target JSON did not contain '{target_config['response_field']}', 'answer', or 'response'."
        )

    sources = parsed.get("sources") or retrieval["sources"]
    context_chunks = parsed.get("context_chunks") or retrieval["context_chunks"]
    return {
        "question": prompt,
        "answer": str(answer),
        "sources": list(dict.fromkeys(sources)),
        "context_chunks": context_chunks,
    }


def execute_target(prompt, runtime_context, *, model_id, target_config, system_prompt=None):
    """Execute the configured application under test and normalize the output."""
    normalized_target = normalize_target_config(target_config)
    mode = normalized_target["mode"]
    if mode == "local_rag":
        return _local_rag(prompt, runtime_context, model_id, system_prompt=system_prompt)
    if mode == "http_json":
        return _http_json(prompt, runtime_context, normalized_target, system_prompt=system_prompt)
    raise ValueError(f"Unsupported target_mode: {mode}")
