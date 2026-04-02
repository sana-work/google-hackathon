# Technical Walkthrough: GenAI Guardrail Factory

## 1. Idea Overview

The **GenAI Guardrail Factory** is a robust, automated platform modeled around the principles of CI/CD, tailored specifically for generative AI applications. It subjects AI models (like Enterprise RAG systems, AI-powered chatbots, etc.) to rigorous red-teaming checks and multi-dimensional safety evaluations *before* they are deployed into production.

The core philosophy is simple: **Just as code requires continuous integration to ensure functional reliability, AI requires continuous evaluation to ensure safety and compliance.**

By utilizing Google AI technologies (Gemini API, Vertex AI Pipelines, Vertex AI Evaluation SDK), the Factory simulates adversarial behaviors—including jailbreaks, hallucinations, and privacy violations—and scores the model's responses to enforce automated pass/fail release gates.

---

## 2. High-Level Architecture

The technical architecture represents an orchestrated data pipeline running primarily on Vertex AI.

```text
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Adversarial     │     │   Target LLM     │     │ Multi-Dimensional│
│  Test Generation │────▶│   Application    │────▶│    Evaluation    │
│  (Gemini API)    │     │   (e.g., RAG)    │     │  (Vertex AI SDK) │
└──────────────────┘     └──────────────────┘     └────────┬─────────┘
                                                           │
                                                           ▼
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ Looker Studio/   │     │ Historical State │     │   Release Gate   │
│ Web Dashboard    │◀────│ (BigQuery)       │◀────│   Decision Engine│
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

The system operates in **five discrete stages**:

1. **Test Generation:** Creates context-aware, adversarial test cases.
2. **Execution:** Injects prompts into the target application and captures the response.
3. **Scoring:** Evaluates the AI response on 6 distinct safety dimensions.
4. **Gating Check:** Compares dimension scores to predefined enterprise thresholds.
5. **Analytics:** Logs the evaluation run for compliance auditing and trend tracking.

---

## 3. Technical Implementation of Core Components

### 3.1 Adversarial Test Generator

Instead of manually crafting edge-case prompts, the Factory relies on **LLMs testing LLMs**.

- **Model:** Gemini 1.5 Pro.
- **Workflow:** Gemini is provided with the target application's context (e.g., HR Policies chunk). It is instructed to generate prompts that push boundaries.
- **Test Categories:**
  - **Hallucination Triggers:** Questions referencing non-existent policies.
  - **Jailbreak Probes:** Attempts to override system instructions ("Ignore previous role...").
  - **PII Extraction:** Intentional queries designed to leak names, SSNs, and emails.
  - **Policy Violation:** Testing restricted topics.
  - **Bias Injections:** Testing fairness and neutrality.

### 3.2 Target Application Execution Layer

This layer is an orchestration script (e.g., Python on Cloud Functions or Vertex Pipelines) that iterates through the generated JSON suite of test cases and submits them to the target model endpoint (the Application Under Test). The responses, along with metadata (latency, tokens), are logged for scoring.

### 3.3 Multi-Dimension Evaluator

The most critical part of the factory. Every test response is scored (0 to 1) using the **Vertex AI Evaluation SDK** combined with **LLM-as-a-Judge** scripts.

1. **Groundedness:** Uses the Vertex AI `groundedness` metric. Checks if the response strictly maps back to the provided source document.
2. **Toxicity & Safety:** Evaluated against safety classifiers for hate speech, harassment, and dangerous content.
3. **Citation Accuracy:** Verifies if the sources cited in the model response match the factual chunks retrieved.
4. **PII / Data Leakage:** A mix of regular expressions (for structured PII like SSN/Emails) and semantic analysis (for unstructured PII) to detect leakage.
5. **Jailbreak Resistance:** Evaluated by Gemini to determine if the target model successfully deflected the adversarial attack or mistakenly role-played the injected persona.
6. **Policy Compliance:** Evaluated against an organizational rulebook (e.g., "AI must not provide legal advice").

### 3.4 Automated Release Gate

A logical evaluation script reads all aggregated dimension scores.

- **Threshold Matching:** E.g., Groundedness must be >= 0.85, PII Leakage >= 0.90.
- **Action:** If all thresholds are met, a deployment flag is triggered in the CI/CD pipeline (e.g., Jenkins or Cloud Build). If a threshold fails, deployment is explicitly blocked and detailed reports are generated.

### 3.5 Storage and Visualization

- **Storage:** **BigQuery** acts as the immutable ledger for evaluations. It holds historical test cases, raw responses, and score telemetry.
- **Visualization:** A multi-layered dashboard (Looker or custom web UI) displays current evaluation status, failed edge cases, and safety progression over time.

---

## 4. Google Cloud Service Mapping

| Technology | Purpose in the Guardrail Factory |
|---|---|
| **Gemini 1.5 Pro API** | Drives the adversarial test generation and acts as the "LLM Judge" for complex custom evaluations like Policy Compliance. |
| **Vertex AI Evaluation SDK** | Provides out-of-the-box, rigorously tested metrics for Groundedness, Toxicity, and Coherence. |
| **Vertex AI Pipelines** | Orchestrates the end-to-end flow. Connects Data Extraction -> Test Generation -> Execution -> Scoring -> Deployment. |
| **BigQuery** | The enterprise data warehouse providing a verifiable, auditable trail of all test executions and scores across model iterations. |
| **Cloud Functions / Cloud Scheduler** | Executes automated monitoring and continuous evaluation intervals once the application hits production. |

---

## 5. Web PoC Technical Stack

For the Hackathon demonstration, the repository now contains a **working web PoC**, not just a static simulation.

### What the PoC actually implements today

- **Backend:** FastAPI orchestration service in Python.
- **Frontend:** A custom HTML, Vanilla JavaScript, and CSS dashboard for stage execution, gating, and remediation review.
- **Model access:** Vertex AI / Gemini calls through the Google Gen AI SDK, plus a deterministic Demo Mode for stable live presentations.
- **Local data path:** Local sample enterprise documents, local chunking, sentence-transformer embeddings, and Chroma vector retrieval for the bundled RAG example.
- **Persistence:** Lightweight persisted run tracking for hackathon-grade replay and reset flows.

### Why this PoC exists

The current implementation is intentionally optimized for **Phase 1 validation**:

1. prove the guardrail workflow end to end,
2. demonstrate release-gate decisions on real generated tests,
3. show Gemini-assisted remediation, and
4. create a credible bridge to a fuller Google Cloud deployment.

### What is PoC scope vs. future platform scope

- **Implemented now:** dashboard-driven stage execution, 3 evaluation dimensions, policy-based release blocking, remediation, persisted runs, and pluggable application-under-test support.
- **Target next on Google Cloud:** Cloud Run hosting, BigQuery history, Scheduler/Tasks for recurring runs, Secret Manager for credentials, and richer enterprise observability and governance.

---

## 6. Future Expansion Roadmap

1. **Integrated Remediation:** Instead of just failing a deployment, the pipeline uses Gemini to dynamically suggest *how* to fix the system prompt or guardrail layer to pass the required test cases.
2. **Real-time Monitoring Hooks:** Creating a lightweight SDK proxy that runs the most critical evaluations (like Toxicity or PII leakage) in milliseconds *during* inference, rather than just pre-deployment.
3. **Cross-Model Benchmarking:** The Factory evaluates identical prompts across Gemini, Claude, and Llama simultaneously to choose the safest foundational model for specific enterprise tasks.
