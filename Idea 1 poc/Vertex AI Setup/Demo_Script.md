# GenAI Guardrail Factory — Hackathon Demo Script

## Demo Goal

Show that the Guardrail Factory can:

1. evaluate a GenAI application end to end
2. generate adversarial attacks automatically
3. apply a real release gate instead of a passive report
4. remediate weak behavior and re-test
5. archive the run as auditable Google Cloud history

This script is designed for the **dashboard-first PoC** that exists in the repository today.

---

## Recommended Demo Mode

Use **Demo Mode (Deterministic)** for the main hackathon presentation.

Why:

- it keeps the exact product flow and UI
- it avoids live-model instability during judging
- it guarantees a stable “blocked -> remediation -> improved posture” story

Keep **Live Vertex Mode** available as a backup proof point for technical Q&A.

---

## Suggested Demo Length

8 to 10 minutes

---

## 1. Opening Problem Statement (~45 sec)

**SAY:**

> "Enterprises are moving fast with GenAI copilots, policy bots, and RAG assistants, but there is still a major gap: most teams do not have an automated release gate for AI safety."
>
> "Today, unsafe behavior is often found manually and too late. Our GenAI Guardrail Factory turns Responsible AI into an operational workflow: generate attacks, evaluate risk, block unsafe release, and recommend a fix."

---

## 2. What The Product Does (~45 sec)

**SHOW:** the dashboard homepage

**SAY:**

> "This product runs a four-stage guardrail workflow:
> 1. initialize the target application and retrieval context
> 2. generate adversarial tests automatically
> 3. evaluate responses against safety dimensions and release policy
> 4. harden the prompt and re-test"

> "This is not just a dashboard. It is an operational release decision engine."

---

## 3. Set Up The Demo (~30 sec)

**SHOW:** left control rail

**DO:**

1. Set **Run Mode** to `Demo Mode (Deterministic)`
2. Leave the default model/judge selections
3. Keep `Tests Per Category` at `5`
4. If BigQuery archive is enabled, point out the archive panel briefly

**SAY:**

> "For the stage demo, I’m using deterministic demo mode so the flow is stable and repeatable. The same interface also supports live Vertex-backed evaluation."

---

## 4. Run Stage 1 — Initialize (~45 sec)

**DO:**

1. Click `Start Fresh Run`
2. Click `Initialize Pipeline`

**SAY:**

> "Stage 1 prepares the evaluation context. In live mode, this loads the document corpus, builds retrieval context, and initializes the model path. In demo mode, it follows the same operator flow with stable fixtures."

**POINT OUT:**

- stage progress
- pipeline timeline
- run controls remain visible

---

## 5. Run Stage 2 — Generate Adversarial Tests (~1 min)

**DO:**

1. Click `Generate Adversarial Tests`

**SAY:**

> "Instead of hand-writing red-team prompts, the system creates adversarial tests across five categories:
> hallucination, jailbreak, PII extraction, policy boundary, and bias injection."

> "This is a big leverage point. The evaluator can continuously generate pressure against the application instead of depending on a static QA spreadsheet."

---

## 6. Run Stage 3 — Evaluate And Gate (~2 min)

**DO:**

1. Click `Run Full Evaluation`

**SAY while it runs:**

> "Now the application is executed against the generated suite and scored across groundedness, toxicity safety, and PII protection."

> "But the important part is what happens next: the system applies a release gate. We are not just measuring scores, we are making a deployment decision."

**WHEN RESULTS LOAD, HIGHLIGHT:**

- verdict banner
- safety dimension cards
- highest-risk category
- failed tests table

**SAY:**

> "This run is blocked because the guardrail policy does more than average scores. It also enforces category floors, critical-failure rules, and scoring-reliability checks."

If the run is blocked:

> "That means the system can stop a risky AI release before it reaches production."

If the run passes:

> "This means the evaluated version currently clears policy. The same system can still be used continuously after every prompt, model, or knowledge-base change."

---

## 7. Show Why The Verdict Matters (~1 min)

**SHOW:**

- `Run Context`
- `Operator Guidance`
- `Pass Rate by Attack Category`
- `Failed Test Cases`

**SAY:**

> "The dashboard is designed for operators, not just judges. It explains what failed, why the run is blocked, and where to focus next."

> "For example, here we can see the weakest category immediately, and we can drill into the exact failing prompts."

If available:

> "We also surface judge reliability, so operators know whether scores came from structured evaluation or fallback logic."

---

## 8. Run Stage 4 — Auto-Remediation (~1.5 min)

**DO:**

1. Click `Run Auto-Remediation`

**SAY:**

> "Now Gemini diagnoses the failure patterns, proposes a stronger system prompt, and the app re-runs the full suite."

> "That full re-test matters. We are not just fixing previously failed prompts in isolation; we are checking whether the proposed fix causes regressions elsewhere."

**WHEN RESULTS UPDATE, HIGHLIGHT:**

- remediation verdict
- before/after cards
- root-cause/fix panels
- improved system prompt

**SAY:**

> "This is the closed loop: detect, block, diagnose, harden, and verify."

---

## 9. Show Google Cloud Value (~1 min)

**SHOW:**

- `PoC Runtime Now / Production Target On Google Cloud`
- `Run Archive` in Run Context if enabled

**SAY:**

> "What you’re seeing today is the working hackathon PoC runtime. It already proves the core workflow."

> "The next production step is to keep this same release-gate logic while moving the control plane and history onto managed Google Cloud services:
> Cloud Run for the API and UI,
> BigQuery for evaluation history,
> Secret Manager for credentials,
> and Scheduler plus Tasks for continuous evaluation."

If BigQuery archive is enabled:

> "This run is also being archived into BigQuery, which gives us an auditable history layer for trends, compliance, and executive reporting."

---

## 10. Closing Positioning (~45 sec)

**SAY:**

> "The differentiator here is not just model evaluation. It is operationalizing AI safety as a release-control system."

> "Instead of asking whether a GenAI app seems safe, teams can continuously test it, score it, gate it, remediate it, and keep a cloud audit trail."

> "That is how GenAI moves from demos to governed enterprise deployment."

---

## Optional Q&A Proof Points

Use these only if judges ask:

- **Live mode exists:** Switch from Demo Mode to `Live Vertex Mode`
- **Target is pluggable:** Show `Application Under Test` supports both the bundled local RAG app and an external HTTP JSON endpoint
- **Judge separation exists:** Show `Judge Model` is configurable independently from the application model
- **Release policy is configurable:** Show category floor, critical-failure allowance, and fallback-score limits

---

## Demo Checklist

Before presenting:

1. Start the server cleanly
2. Hard refresh the browser
3. Confirm `Start Fresh Run` works
4. Confirm `Demo Mode (Deterministic)` is selected
5. Optionally enable BigQuery archive if dependencies and API access are ready
6. Run one rehearsal end to end

---

## Fallback Plan

If anything goes wrong live:

1. Click `Start Fresh Run`
2. Stay in `Demo Mode`
3. Re-run Initialize -> Generate -> Evaluate -> Remediate

If judges ask whether it works with real services:

> "Yes. The same product supports live Vertex mode as the real evaluation path. Demo mode is used here to make the on-stage walkthrough deterministic and reliable."
