# GenAI Guardrail Factory

## Automated Red-Teaming & Evaluation Pipeline for Responsible AI

**Google AI Track:** Build with Vertex AI  
**Submission Date:** February 2026  
**tcs^AI Google Hackathon 2026 — Ideathon Phase**

---

## 1. Executive Summary

The **GenAI Guardrail Factory** is an automated platform that treats Responsible AI like CI/CD — providing systematic, repeatable testing of GenAI applications for hallucinations, data leakage, policy violations, jailbreaks, and unsafe outputs before production deployment. Just as no enterprise deploys code without unit tests, no GenAI application should deploy without guardrail tests.

---

## 2. Problem Statement

### The Challenge

Enterprises are rapidly deploying GenAI applications — chatbots, RAG systems, AI-powered agents, and copilots. However, **there is no standardized, automated framework to test these systems for safety, accuracy, and compliance** before they reach production.

### Current State

| Aspect | Today's Reality |
|--------|----------------|
| **Testing approach** | Manual, ad-hoc, inconsistent |
| **Coverage** | Incomplete — teams test for "happy paths" only |
| **Frequency** | One-time before launch, no continuous monitoring |
| **Standards** | No unified evaluation criteria across teams |
| **Governance** | No auditable evidence of safety testing |

### Consequences of Inaction

- **Hallucinated responses** damage customer trust and decision-making
- **PII/data leakage** creates compliance violations (GDPR, DPDPA, HIPAA)
- **Jailbreak vulnerabilities** expose enterprise systems to prompt injection attacks
- **Policy violations** lead to brand and legal risks
- **Lack of audit trail** makes regulatory compliance impossible to demonstrate

### Who Faces This Problem?

Every enterprise deploying GenAI — across BFSI, healthcare, telecom, manufacturing, and government. This is especially critical for TCS, which deploys AI solutions across hundreds of client accounts, each with unique compliance requirements.

---

## 3. Proposed Solution

### Core Concept

The GenAI Guardrail Factory is a **reusable, automated evaluation pipeline** built on Vertex AI that acts as a quality gate for any GenAI application. It systematically generates adversarial tests, evaluates responses across multiple safety dimensions, and produces a pass/fail release gate with full auditability.

### Key Capabilities

#### 3.1 Adversarial Test Suite Generator

- Automatically generates diverse, contextually relevant test cases targeting known failure modes
- **Test categories include:**
  - Hallucination triggers (questions with no answer in the knowledge base)
  - Jailbreak prompts (role-play attacks, instruction override attempts)
  - PII extraction probes (attempts to extract sensitive data from context)
  - Policy boundary tests (requests that push against organizational guardrails)
  - Bias-inducing inputs (prompts designed to elicit biased or unfair responses)
- Uses **Gemini API** to generate domain-specific adversarial inputs based on the target application's context

#### 3.2 Multi-Dimensional Evaluation Engine

Each test case is run through the target GenAI application and scored across **6 safety dimensions:**

| Dimension | What It Measures | How It's Scored |
|-----------|-----------------|-----------------|
| **Groundedness** | Is the response supported by source documents? | 0-1 score via Vertex AI Evaluation SDK |
| **Toxicity & Safety** | Harmful, offensive, or inappropriate content | Binary flag + severity score |
| **PII/Data Leakage** | Does the response expose sensitive information? | Pattern matching + semantic detection |
| **Citation Accuracy** | Are sources correctly referenced? | Automated verification against source docs |
| **Policy Compliance** | Does it follow organization-specific rules? | Custom policy checklist evaluation |
| **Jailbreak Resistance** | Can it be tricked into bypassing instructions? | Adversarial success rate measurement |

#### 3.3 Release Gate & Dashboard

- Aggregates dimension scores into an overall **pass/fail release gate**
- Configurable thresholds per dimension (e.g., "Groundedness must be ≥0.85")
- **Visual dashboard** showing:
  - Current evaluation results with drill-down
  - Trend lines across evaluation runs over time
  - Comparison across application versions
  - Risk heat maps by dimension

#### 3.4 Continuous Monitoring

- Post-deployment, the pipeline runs on a **configurable schedule** against production endpoints
- Detects safety regression when models are updated or knowledge bases change
- Automated alerting when scores drop below thresholds

---

## 4. Architecture

### System Architecture Diagram

![GenAI Guardrail Factory - Architecture Diagram](/Users/sanaiqbal/.gemini/antigravity/scratch/tcs-hackathon-2026/guardrail_factory_architecture.png)

### Data Flow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────────┐    ┌────────────┐    ┌───────────┐
│  Adversarial │───▶│  Target      │───▶│  Multi-Dimension │───▶│  Release   │───▶│ Dashboard │
│  Test        │    │  GenAI       │    │  Evaluator       │    │  Gate      │    │ & Reports │
│  Generator   │    │  Application │    │  (6 dimensions)  │    │ (Pass/Fail)│    │           │
└──────────────┘    └──────────────┘    └──────────────────┘    └────────────┘    └───────────┘
     │                                          │                     │                 │
     │            Vertex AI Pipelines (Orchestration Layer)           │                 │
     └──────────────────────────────────────────┴─────────────────────┴─────────────────┘
                                                │
                    ┌───────────────┬────────────┼────────────┬──────────────┐
                    │               │            │            │              │
              Gemini API    Vertex AI Eval   BigQuery     Looker     Cloud Functions
              (Test Gen)    SDK (Scoring)    (History)    (Viz)      (Scheduling)
```

### Google AI Technology Stack

| Component | Google Service | Purpose |
|-----------|---------------|---------|
| Pipeline Orchestration | **Vertex AI Pipelines** | End-to-end workflow management |
| Test Generation | **Gemini API** | Generate adversarial test cases |
| Response Evaluation | **Vertex AI Evaluation SDK** | Score groundedness, safety, coherence |
| Custom Evaluation | **Gemini API** | Policy compliance & citation checks |
| Data Storage | **BigQuery** | Evaluation history & trend analysis |
| Visualization | **Looker / Cloud Dashboard** | Pass/fail gates & trend visualization |
| Scheduling | **Cloud Functions + Cloud Scheduler** | Automated continuous evaluation |
| Authentication | **Cloud IAM** | Role-based access control |

### Current Repository Status

The current codebase should be read as a **Hackathon PoC implementation of Phase 1**, not as a full deployment of the entire Google Cloud target architecture shown above.

- **Implemented in the repo now:** a working FastAPI + web dashboard control plane, real Vertex/Gemini-backed evaluation paths, deterministic Demo Mode, persisted run state, release gates, remediation, and a bundled local RAG sample application.
- **Still a target architecture:** Vertex AI Pipelines orchestration, BigQuery as the long-term analytics ledger, Looker-based reporting, Cloud Scheduler-driven continuous evaluation, and fuller IAM/governance layers.

---

## 5. Implementation Approach

### Phase 1: PoC (2-3 weeks)

- Build core pipeline: Test Generation → Evaluation → Scoring → Report
- Implement 3 evaluation dimensions: Groundedness, Toxicity, PII Leakage
- Create 50 adversarial test cases for a sample RAG application
- Build a simple dashboard showing pass/fail results
- Deliver a demo-safe mode so judges can see the same workflow even if live model behavior becomes noisy

### Phase 2: MVP (4-6 weeks)

- Add all 6 evaluation dimensions
- Implement configurable thresholds and release gates
- Add trend analysis and version comparison
- Integrate with CI/CD tools (Cloud Build, Jenkins)

### Phase 3: Production Platform (8-12 weeks)

- Multi-tenant support for multiple teams/applications
- Custom policy rule engine
- Continuous monitoring with alerting
- Integration with enterprise governance tools
- API for programmatic access

### Key Milestones

```
Week 1-2:  Core pipeline + 3 eval dimensions + test suite
Week 3:    Dashboard + release gate logic
Week 4-6:  All 6 dimensions + trend analysis + CI/CD integration
Week 7-12: Multi-tenant + monitoring + enterprise integrations
```

---

## 6. Novelty & Differentiation

| Aspect | Existing Solutions | GenAI Guardrail Factory |
|--------|--------------------|----------------------|
| **Approach** | Manual testing by developers | Automated, systematic, repeatable |
| **Coverage** | Ad-hoc test cases | 6 structured safety dimensions |
| **Frequency** | One-time pre-launch | Continuous monitoring |
| **Output** | Informal feedback | Auditable pass/fail gate + reports |
| **Scope** | Single application | Platform serving all GenAI projects |
| **Analogy** | "Hope it works" | CI/CD for Responsible AI |

### Why This Idea Is Unique

1. **Meta-AI**: This is AI that tests AI — a layer most teams aren't building
2. **Security IS the product**: Directly addresses the 15% rubric weight for Security & Compliance
3. **Enterprise-grade governance**: Audit trails, version tracking, approval workflows
4. **Reusable platform**: Build once, use across every GenAI project in the organization

---

## 7. Business Value

### Quantitative Impact

- **60-80% reduction** in time spent on manual GenAI safety testing
- **90%+ coverage** of known adversarial attack vectors (vs. <20% with manual testing)
- **Prevents costly production incidents** — each GenAI failure costs $50K-$500K in remediation + reputation damage

### Strategic Value for TCS

- **Differentiator**: Offer clients a "Responsible AI Certification" for their GenAI deployments
- **Scalable**: One platform serves hundreds of client GenAI projects
- **Revenue opportunity**: Can be offered as a managed service ("Guardrails-as-a-Service")
- **Regulatory readiness**: Positions TCS ahead of EU AI Act compliance requirements

### Long-term Sustenance

- As GenAI adoption grows, the need for automated safety testing **only increases**
- New adversarial patterns are continuously added, keeping the platform relevant
- Applicable across all LLM providers (Gemini, GPT, Claude, open-source models)

---

## 8. Security & Compliance

| Aspect | Implementation |
|--------|---------------|
| **Access Control** | Cloud IAM role-based access; team-level isolation |
| **Data Privacy** | No production/client data used in testing; synthetic adversarial inputs only |
| **Audit Trail** | Every evaluation run logged: who tested, what version, when, results |
| **Model Tracking** | Model version + prompt version tracked for reproducibility |
| **Approval Workflows** | Release gate overrides require authorized approval |
| **PII Protection** | Built-in PII detection and redaction in test inputs/outputs |
| **Compliance Alignment** | Google Responsible AI Principles, EU AI Act readiness, NIST AI RMF |

### Responsible AI Practices

- **Transparency**: All evaluations are explainable with specific evidence
- **Fairness**: Includes bias detection in adversarial test suites
- **Accountability**: Clear ownership and approval chains for release decisions
- **Human-in-the-loop**: Automated testing informs, humans make final deployment decisions

---

## 9. PoC Demonstration Plan

### What the PoC Includes

1. **Sample RAG Application**: A simple question-answering system over synthetic enterprise documents
2. **Adversarial Test Suite**: 50 test cases across 3 categories (hallucination, PII extraction, jailbreak)
3. **Evaluation Pipeline**: Automated scoring for groundedness, toxicity, and PII leakage
4. **Release Gate**: Pass/fail determination with configurable thresholds
5. **Dashboard**: Visual report showing scores, trends, and drill-down details

### PoC Demo Flow

```
Step 1: Show the target RAG application working normally
Step 2: Run the Guardrail Factory pipeline against it
Step 3: Display adversarial test results — some pass, some fail
Step 4: Show the release gate decision (e.g., "FAIL — PII leakage score 0.6 < threshold 0.9")
Step 5: Fix the application (add better guardrails)
Step 6: Re-run the pipeline — now passes all gates
Step 7: Show trend dashboard comparing before/after
```

---

## 10. References & Inspiration

- Google Responsible AI Practices: <https://ai.google/responsibility/responsible-ai-practices/>
- Vertex AI Evaluation SDK: <https://cloud.google.com/vertex-ai/docs/generative-ai/models/evaluate-models>
- NIST AI Risk Management Framework: <https://www.nist.gov/artificial-intelligence/ai-risk-management-framework>
- EU AI Act Requirements: <https://artificialintelligenceact.eu/>

---

*This document is submitted as part of the tcs^AI Google Hackathon 2026 — Ideathon Phase. All data used is synthetic. No real client names, PII, or confidential information is included.*
