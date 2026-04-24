# TCS^AI Google Hackathon 2026: Final Presentation Guide
**Customized for Idea 1: GenAI Guardrail Factory**

Congratulations on making it to the Top 10 for the final stage of the Hackathon! This guide explains exactly how to fill out the standard 14-slide presentation template, specifically tailored to the **GenAI Guardrail Factory** project (Track: Build with Vertex AI).

## General Ground Rules
1. **Show, Don't Tell:** Use high-resolution, cropped screenshots from inside the Fresco Play lab to show the Guardrail Factory dashboard and evaluation pipeline. 
2. **Keep Text Short:** No slide should have more than ~40 words of body text. Speak to the details.
3. **Data Privacy (Hackathon Rules):** Do not use real client names, logos, PII, or client documents. Emphasize that your solution uses synthetic adversarial inputs.
4. **Delivery:** Don't read the slides aloud. Use slides as evidence; speak to the insight.

---

## Slide-by-Slide Content Guide

### Slide 1: Cover
* **Use Case Title:** Automated GenAI Guardrail Factory
* **Team:** [Your Team Name]
* **Track:** Build with Vertex AI

### Slide 2: Agenda
* **What to include:** Standard agenda. No specific edits needed.

### Slide 3: Team & Track *(Delete if pressed for time)*
* **Our Track:** Build with Vertex AI
* **Why We Chose It:** 
  1. Vertex AI Evaluation SDK perfectly fits our multi-dimensional testing needs.
  2. Gemini API excels at dynamically generating contextual adversarial inputs.
  3. Vertex AI Pipelines enable enterprise-ready orchestration and scale.

### Slide 4: The Problem *(Problem Fit - 20%)*
* **Who Is Affected:** Enterprise AI Deployment Teams & Compliance Officers across BFSI, Healthcare, and Govt.
* **The Problem:** Teams are deploying GenAI applications without automated, standardized testing for hallucinations, data leakage, and jailbreaks—relying on incomplete, ad-hoc manual testing.
* **Quantified Stats:**
  * `[80%]` of stakeholder time lost to manual, incomplete GenAI safety testing.
  * `[$250K]` average remediation cost/revenue leakage per production AI incident.
  * `[<20%]` test coverage of known adversarial attack vectors with current manual processes.

### Slide 5: Our Solution *(Novelty - 15% + Problem Fit - 20%)*
* **Elevator Pitch:** We built the GenAI Guardrail Factory—a dynamic, multi-layered "release gate" agent. Instead of a basic API wrapper, it uses the Google Agent Development Kit (ADK) to dynamically evaluate, score, and remediate target AI outputs against strict enterprise thresholds before deployment.
* **3 Differentiators:** 
  1. **Agentic Routing:** The ADK `LlmAgent` routes to precise Python functions to calculate deterministic security scores.
  2. **CI/CD for Responsible AI:** Automated pass/fail release gates based on 6 safety dimensions.
  3. **Enterprise-Grade Governance:** Full audit trails, version tracking, and config-driven policies.

### Slide 6: Solution in Action *(Evidence - 10%)*
* **Screenshot:** Provide a high-resolution screenshot of the Guardrail Factory Web Dashboard showing a Pass/Fail run.
* **4-Step User Journey:**
  1. **Trigger:** Pipeline scheduled or triggered via CI/CD for a target GenAI app.
  2. **Generate:** Gemini API dynamically creates 50+ adversarial test cases (hallucinations, jailbreaks).
  3. **Evaluate:** Vertex AI Evaluation SDK scores responses across 6 safety dimensions.
  4. **Deliver:** Visual dashboard presents a strict pass/fail release gate with drill-down audit logs.

### Slide 7: Architecture *(Implementation - 20% + Long-term Value - 20%)*
* **Screenshot:** End-to-end GCP architecture diagram (from your documentation).
* **Key Components:**
  * **Front-end / Channel:** Enterprise Application payload via FastAPI Backend Server.
  * **Agent Layer:** Google ADK `GuardrailEvaluatorAgent` evaluating via Vertex AI.
  * **Tools & Webhooks:** PII Leakage Scanner, Toxicity Evaluator, Groundedness Checker.
  * **Data / Grounding:** ChromaDB Vector Store for strict context retrieval.

### Slide 8: Under the Hood *(Novelty - 15%)*
* **Capabilities beyond a wrapper:**
  * **Custom Tool Calling:** The `LlmAgent` relies on precise Python functions (e.g., `check_pii_leakage`) rather than just LLM semantics.
  * **Multi-Dimensional Scoring:** Parallel evaluation across **Hallucination, PII Extraction, Jailbreak/Role Override, Toxicity, and Policy Violation**.
  * **Automated Release Gates:** Strict threshold enforcement (e.g., **Groundedness >= 0.850**).
  * **Auto-Remediation Pipeline:** BLOCKED → DIAGNOSE → HARDEN → APPROVED loop. Actively generates "Hardened Prompts" (e.g., adding explicit PII/RAG grounding rules).

### Slide 9: Proof of Execution *(Implementation - 20% + Evidence - 10%)*
*(Track 2 - Build with Vertex AI Specifics)*
* **Build (Screenshot):** Terminal showing `adk run Vertex_ADK_Agent` and the local interactive loop successfully failing a test on "Vikram's PII: vikram@email.com" using custom tools.
* **Deploy (Screenshot):** Terminal showing successful execution of `adk deploy agent_engine --name guardrail-evaluator --region us-central1` and containerizing the agent.
* **Validate (Screenshot):** Google Cloud Console showing your `guardrail-evaluator` deployed AND a live Playground test query enforcing a validated Groundedness score and feedback.

### Slide 10: Security & Guardrails *(Security - 15%)*
* **PII & Data Privacy:** Built-in semantic PII detection blocks real data extraction; uses strictly synthetic adversarial inputs for testing. **Categorical PII prohibition** added to system instructions.
* **Grounding & Citations:** Vertex AI Evaluation SDK enforces a rigorous **0.850 threshold**. Detects and blocks "plausible-sounding but unsupported" answers.
* **Human-in-the-Loop:** Automated pipeline informs decisions; **Audit Trail** logs every authorized operator run (e.g., Sana Iqbal, EID: 1213383).
* **Domain Boundaries:** Strict authority boundaries prevent unauthorized approvals/actions (e.g., "Direct all action requests to the HR portal").

### Slide 11: Scale & Enterprise Readiness *(Long-term Value - 20%)*
* **Modular Architecture:** Vertex AI Pipelines allow horizontal scaling for thousands of parallel test evaluations. Multi-tenant design isolates team data.
* **Reuse Map:** 
  * Applicable across BFSI, Healthcare, Telecom, and Government.
  * Scales to test any LLM provider (Gemini, Claude, open-source models).
  * Can be offered as "Guardrails-as-a-Service" for hundreds of client projects.

### Slide 12: Business Impact
* **KPI Callouts:**
  * **70% reduction** in manual GenAI safety testing cycle time.
  * **$250K+ average cost saved** per prevented production hallucination incident.
  * **90%+ test coverage** of adversarial vectors.
  * **100% auditability** (Immutable run records logged to BigQuery).
* **Qualitative Impact:**
  * **Employee:** Shifts engineers from manual testing to high-judgment remediation (e.g., fixing 8+ active failure patterns in minutes).
  * **Customer:** Ensures 24x7 accurate response with source-grounded citations.
  * **Risk Posture:** Zero-tolerance PII policy and auditable "BLOCKED" decisions provide absolute compliance.

### Slide 13: What's Next
* **4-Milestone Roadmap:**
  1. Core Pipeline (3 dimensions + Test Suite)
  2. MVP (6 dimensions + Release Gates)
  3. CI/CD Integration & Trend Analysis
  4. Multi-tenant Enterprise Platform with Alerting
* **Our Ask from Google:** "Guidance on scaling Vertex AI Evaluation SDK quotas for massive enterprise-wide parallel testing."

### Slide 14: Thank you / Q&A
* **Closing Slide:** Keep contact details visible.

---

## Pitch Time Budget (10-12 Minutes)
* **Open (1 min):** Slides 1 & 3
* **Problem (1 min):** Slide 4
* **Solution + Demo (3-4 min):** Slides 5 & 6 *(The star of the show - focus on the automated red-teaming)*
* **Architecture + Novelty + Proof (3 min):** Slides 7, 8, & 9
* **Security, Scale, Business Impact (2 min):** Slides 10, 11, & 12
* **Roadmap + Ask + Thank You (1 min):** Slides 13 & 14
* **Q&A:** Remaining time
