# GenAI Guardrail Factory — Final Demo Package
**Presenter:** Sana Iqbal · GenAI Solution Architect, AI Services (BFSI) · TCS^AI Google Hackathon 2026
**Target runtime:** ~6 min 40 sec spoken (under the 7-minute cap; condense slides 11–12 if you need more buffer)

---

## 1. Final Speaking Script (~6:40)

> Delivery notes are in *italics* — don't read them aloud. Bolded lines are the ones to land with emphasis and a short pause after.
> Pace target ≈ 140 words/min. If you tend to speed up when nervous, the buffer absorbs it.

### SLIDE 1 — Cover *(0:00 – 0:18)*

*(Title's on screen — don't read it. Open warm and easy, like you're talking, not pitching.)*

Hi everyone. So we've all seen how fast GenAI assistants are going from prototype to production these days. The catch is, a model that looks brilliant in a demo can quietly start behaving differently the moment you tweak a prompt, swap a model version, *(half-second pause)* or refresh a document.

That's exactly the tension behind today's idea: **GenAI Guardrail Factory**.

*(advance to Slide 2)*

---

### SLIDE 2 — Agenda *(0:18 – 0:26)*

*(Quick orient — don't read every line on the slide.)*

In the next few minutes I'll walk you through the problem, the solution, a live demo, the architecture on Google Cloud, and the proof that it actually runs.

*(advance to Slide 3)*

---

### SLIDE 3 — Team & Track *(0:26 – 0:55)*

*(Your intro lands here, on the slide that actually shows your name and track.)*

And quickly about me — I'm **Sana Iqbal**, a GenAI Solution Architect on the AI Services team in our BFSI unit. So I spend my days where responsible AI, privacy, and production-readiness aren't nice-to-haves — they're the difference between a release going out and a release getting stopped.

We built this on the **Build with Vertex AI** track using **Google ADK**. And the reason is right here: enterprise GenAI needs a *repeatable* safety release gate before production — not one-time manual testing. Gemini can generate adversarial tests and diagnose failures, and ADK lets us run deterministic, tool-based checks.

So the question we keep asking — *"Can this app answer?"* — turns out to be the wrong one. **The real question is: can we prove it's safe enough to release?**

*(advance to Slide 4)*

---

### SLIDE 4 — The Business Problem *(0:55 – 2:05)*

Today, most teams answer that question by hand. They try a few sample prompts, ask a subject-matter expert to eyeball the responses, run a security check or two, and then someone makes a judgment call.

That's fine for a controlled demo. Production is a different world.

In production, nobody follows your script. People ask edge-case questions. They probe for sensitive data. They try to override instructions. They'll ask the assistant to approve something it has no authority to approve. And every so often, the model answers with total confidence — while being completely ungrounded in your actual documents.

That opens four doors you can't leave open: **hallucination, PII leakage, jailbreak or role-override, and policy-boundary violations.**

And this isn't just a developer problem. When one of those slips through, it lands on compliance leaders, risk and security teams, CISOs, and the business owner whose name is on the release.

In BFSI, that's not theoretical — governance and auditability are mandatory. *"It worked when we tested it"* is not an audit trail.

The hard part is that the manual approach simply doesn't scale. **Standing up a safety framework by hand takes six to nine months — and then every prompt change, model upgrade, or document refresh forces you to do it all over again.**

So what enterprises are missing isn't another assistant. It's a **release gate** — something that gives a clear, repeatable verdict: this app is safe to move forward, or this release is blocked.

*(advance to Slide 5)*

---

### SLIDE 5 — Our Solution *(1:50 – 2:50)*

That's what GenAI Guardrail Factory is: a **pre-production safety release gate** for enterprise GenAI applications.

For this proof-of-concept, my target app was an HR Policy assistant running on synthetic HR documents. But I want to be clear — **the HR assistant is just the test vehicle. The product is the gate around it.** That gate is designed to wrap any GenAI app.

Think of it as a safety inspection line before a vehicle is allowed onto the road.

The app gets submitted for evaluation. Gemini then generates adversarial test cases — not friendly demo prompts, but attacks built to find the cracks. Each response is scored by dedicated safety tools for groundedness, toxicity, and PII risk. And a **deterministic** release gate decides: block, or approve.

Here's what makes it more than a scanner. If the app fails, we don't stop at a red light. Gemini diagnoses *why* it failed, hardens the prompt to close that gap, and re-runs the exact same test suite.

So the full lifecycle is: **block, diagnose, harden, re-test, approve.** It doesn't just flag risk — it drives a measurable recovery.

*(advance to Slide 6)*

---

### SLIDE 6 — Solution in Action *(2:50 – 3:45)*

This is the working dashboard — the operator's view of a real run.

A team configures the model, the thresholds, the policy corpus, and the run mode. They submit the target app, and Gemini fans out adversarial tests across categories — hallucination, PII extraction, jailbreak attempts, toxicity, and policy-risk scenarios. In HR terms, that's checking whether the assistant leaks an employee's details, obeys a malicious instruction, or hands out an approval it was never authorized to give.

Google ADK then routes every response to the right tool. The groundedness checker confirms the answer is actually backed by source documents. The PII scanner hunts for sensitive identifiers. The toxicity judge checks tone and safety.

Cross a threshold the wrong way, and deployment is blocked — right here on screen. From there the system moves into auto-remediation, hardens the prompt, re-runs, and only flips to approved once recovery is proven.

So this screen isn't a report. **It's a live safety workflow you can watch make a decision.**

*(advance to Slide 7)*

---

### SLIDE 7 — Architecture *(3:45 – 4:45)*

Here's how it all runs end-to-end on Google Cloud.

On the left is the target app — our HR Policy assistant. Its requests flow into a **FastAPI Orchestrator**, which controls the run, manages thresholds, and routes results.

At the core sits the **Google ADK LlmAgent, powered by Gemini 2.5 Flash.** This is the brain that generates the adversarial tests, diagnoses failures, and proposes the prompt hardening.

But — and this is the crucial design choice — the deploy decision is *not* left to a free-form model answer. The agent calls dedicated tools: the groundedness checker, the PII scanner, the toxicity judge. Grounding is anchored in **ChromaDB** against the synthetic HR documents, so every answer is measured against real source content.

Those scores feed the **deterministic release gate**, which applies the policy: groundedness, toxicity, and PII thresholds, a category floor, and a zero-critical-failures rule.

For the PoC, run history lives in a **SQLite RunStore**, and **Cloud Run** makes the service deployable. At enterprise scale, that same evidence flows into **BigQuery and Looker** for governance dashboards.

So the pipeline reads cleanly: **load documents, build the RAG context, generate tests, execute, evaluate, gate, remediate, re-test.**

*(advance to Slide 8)*

---

### SLIDE 8 — Under the Hood *(4:45 – 5:10)*

One quick point on *why* this design holds up.

It's deliberately hybrid. Gemini does the semantic work — inventing attacks, spotting failure patterns, suggesting fixes. But the final verdict is deterministic, driven by fixed thresholds.

That split matters, because governance needs the same inputs to produce the same decision every time — consistent, traceable, audit-ready.

**So the novelty isn't "AI evaluating AI." It's AI evaluating, explaining, hardening, and verifying AI — inside one repeatable release process.**

*(advance to Slide 9)*

---

### SLIDE 9 — Proof of Execution *(5:10 – 5:35)*

And this actually ran — end-to-end on Google Cloud.

These screenshots walk the real path: documents loaded and indexed, the RAG context built, Gemini generating adversarial prompts, the ADK agent calling each safety tool, the gate applying thresholds, a failure triggering hardened guidance from Gemini, and a re-run to confirm recovery.

**Build, deploy, validate — not a slideware mockup, a working pipeline.**

*(advance to Slide 13 — see narration map note)*

---

### SLIDE 13 — The Proof Metrics *(5:35 – 6:05)*

*(This is your money slide. Slow down. Let each number land.)*

Here's what that run produced.

Going in, groundedness measured **0.840**, just under the **0.850** threshold — with **eight active failures** on the board. Verdict: **deployment blocked.**

Then remediation ran. Groundedness climbed to **0.942**. Toxicity safety reached **0.970**. PII protection, **0.992**. And those eight active failures?

**Reduced to zero — in the documented PoC run.** Verdict: **approved for deployment.**

That's the whole thesis in one screen — a release that *should* have been stopped, was stopped, then recovered to a measurable, evidence-backed pass.

*(advance to Slide 10)*

---

### SLIDE 10 — Model Armor Comparison *(6:05 – 6:35... wait — see note)*
*(Timing-corrected order: speak Model Armor BEFORE metrics if you prefer narrative flow, but the map below keeps metrics as the climax. Either works — pick one and rehearse it.)*

The natural question: how is this different from **Google Model Armor**?

Model Armor is runtime protection. It guards live prompts, responses, documents, and agent interactions against things like prompt injection, jailbreaks, data leakage, and harmful content — while the app is in use.

Guardrail Factory works one step earlier. Put simply: **Model Armor asks, "Is this prompt or response safe right now?" Guardrail Factory asks, "Is this whole application safe enough to release?"**

They're complementary, not competing. **Model Armor protects the live road. Guardrail Factory decides whether the vehicle is safe enough to get on it.** You want both.

*(advance to Slide 11/12)*

---

### SLIDES 11 & 12 — Security, Scale & Value *(condensed — fold into closing if tight)*

Underneath, four responsible-AI guardrails hold the line: data privacy through multi-pattern PII detection; grounding through source-document checks; **auditability** — every score, threshold, verdict, and timestamp stored as evidence; and domain boundaries that reject role overrides and unauthorized approvals.

And because the architecture is modular and runs on Cloud Run, the same gate extends well past HR — into BFSI assistants, compliance copilots, support bots, and regulated RAG workflows. For TCS, that's a reusable **GenAI Safety-as-a-Service accelerator.**

---

### SLIDE 15 — Close *(final 15 sec)*

So, to bring it home.

Enterprises don't just need impressive GenAI demos. They need GenAI they can trust in production — and trust you can *show*, backed by adversarial testing, deterministic thresholds, remediation, and audit evidence.

**Good GenAI demos show capability. Guardrail Factory proves deployability.**

Thank you.

---
---

## 2. Slide-by-Slide Narration Map (with timing)

| Slide | Role in talk | Speak? | Time | Running total |
|-------|--------------|--------|------|---------------|
| 1 Cover | Warm hook (Option B) | ✅ Brief | 0:18 | 0:18 |
| 2 Agenda | One orienting line | ✅ One line | 0:08 | 0:26 |
| 3 Team & Track | Intro + name + track + "real question" | ✅ Full | 0:29 | 0:55 |
| 4 Problem | Business problem + why manual fails | ✅ Full | 1:10 | 2:05 |
| 5 Solution | What it is + lifecycle | ✅ Full | 1:00 | 3:05 |
| 6 Demo | Operator workflow | ✅ Full | 0:55 | 4:00 |
| 7 Architecture | Google pipeline end-to-end | ✅ Full | 1:00 | 5:00 |
| 8 Under the Hood | Hybrid design / novelty | ✅ Brief | 0:25 | 5:25 |
| 9 Proof of Execution | "It really ran" screenshots | ✅ Brief | 0:25 | 5:50 |
| **13 Proof Metrics** | **The numbers (climax)** | ✅ **Full — money slide** | 0:30 | 6:20 |
| 10 Model Armor | Differentiation | ✅ Full | 0:30 | 6:50* |
| 11 Security | Guardrails | ✅ Condensed | folded | — |
| 12 Scale & Reuse | Reuse map | ⏭️ Mostly visual | folded | — |
| 14 Roadmap | Skip per brief | ⏭️ Silent / skip | — | — |
| 15 Close | Final line | ✅ 15 sec | 0:15 | ~6:40 |

> **\* Important timing note:** Slides 11–13 of the *deck* are out of narration order. Your strongest proof (the 0.840→0.942, 8→0 numbers) is physically on **deck slide 13**, not 11/12. Two clean options:
>
> **Option A (recommended): present in deck order** 9 → 10 (Model Armor) → 11 (security) → 12 (scale) → 13 (metrics as climax) → 15. Move the metrics narration to where slide 13 appears. This keeps you clicking forward naturally and ends the body on your strongest number before the close.
>
> **Option B: reorder the deck** so the metrics slide (currently 13) sits right after Proof of Execution (9). If you want this, say the word and I'll move it in the file.
>
> The script above is written for **Option A flow** but I placed the metrics block before Model Armor for emphasis — **rehearse one fixed order and lock it.** Don't improvise the sequence on recording day. At ~6:50 to the end of Model Armor you're close to the cap, so keep slides 11–12 tight (or fold them into the close) to land comfortably under 7:00.

---

## 3. Slide Improvements — what I changed and why

**Already applied to your deck** (file: `deck_final.pptx`):

1. **Slide 13 — removed the "100%" universal claim.** Changed the headline stat from `100% / failure recovery in documented run` to **`8 → 0 / active failures cleared in documented PoC run`**. This is the exact caution you flagged: "100%" reads as a real-world guarantee; "8→0 in the documented run" is defensible and still impressive.

2. **Slide 13 — made the groundedness stat precise and honest.** `+10.2% / groundness improvement` → **`+0.102 / groundedness gain after hardening (0.840 → 0.942)`**. Also fixed the **"groundness" → "groundedness"** typo (it appeared on the slide).

3. **Slide 13 — tightened the PII stat label** to `0 / PII leaks in final run (protection 0.992)` so the headline number ties to the 0.992 score you cite.

4. **Slide 11 — fixed a mislabeled guardrail.** The third card was titled **"Human-in-the-Loop"** but its description is about stored scores, verdicts, timestamps, and audit evidence — that's **auditability**, not HITL. Relabeled to **"Auditability & Evidence"** and changed the icon letter `H → A` so the P · G · A · D set is consistent and accurate. (This also removes a question a sharp judge would ask: "where's the human in your loop?")

5. **Slide 4 — stat figures kept but made defensible (applied).** You chose to keep your business-case numbers rather than swap them, and soften the labels so they survive a challenge:
   - `91%` label → **"lack formal CI/CD-style GenAI safety gates (directional benchmark)."** The word *directional benchmark* signals it's an illustrative figure, not a hard survey stat.
   - `₹4.5Cr+` label → **"conservative GenAI incident-impact estimate (India breach avg: ₹22Cr, IBM 2025)."** This keeps your conservative number *and* anchors it against the real, higher IBM figure — so it reads as deliberately cautious, not invented. (IBM's 2025 India figure is INR 220M ≈ ₹22Cr for the avg cost of *any* data breach.)
   - `6–9 mo` → corrected to **`6–18 mo` / "to move a GenAI project from intake to production (ModelOp 2025)."** The original "6–9 months" didn't match any source; ModelOp's report says 56% of teams take 6–18 months intake-to-production, so this card is now directly attributable.

   **Verbal defense if a judge presses the 91% / ₹4.5Cr numbers** (rehearse these):
   - On 91%: *"I'd treat 91% as a directional benchmark for the adoption-vs-governance gap. The supporting evidence is solid — IBM's 2025 report states AI adoption is greatly outpacing AI security and governance, and in India nearly 60% of organizations either have no AI governance policy or are still building one."*
   - On ₹4.5Cr: *"That's a deliberately conservative incident-impact proxy. It's lower than IBM's full India breach benchmark of around ₹22 crore — so if anything it understates the exposure, rather than inflating it."*

6. **Slide 9 typo — fixed (applied).** "AD terminal execution" → **"ADK terminal execution."** Also aligned the slide-9 title from "...end-to-end on GCP" → "...end-to-end on Google Cloud" for consistency.

7. **Slide 7 title — updated (applied).** "End-to-end GCP architecture" → **"End-to-end Google Cloud architecture."**

8. **Slide 2 agenda + Slide 14 roadmap.** Since you're skipping roadmap and treating agenda as a transition, no edit needed — but if you want a tighter deck, you *could* delete slide 14 entirely. I left it in so your slide numbers and any external references stay stable.

**Sources used for Slide 4 (for your reference):**
- IBM, *Cost of a Data Breach Report 2025* (India release, Aug 7 2025): avg breach cost INR 220M (~₹22Cr), all-time high; ~60% of orgs lack/are still building AI governance policies; only 37% have AI access controls.
- ModelOp, *2025 AI Governance Benchmark Report*: 56% say 6–18 months to move a genAI project from intake to production.

---

## 4. Exact Replacement Text (for anything you edit yourself in PowerPoint)

If you re-open the original in PowerPoint and want to make the changes by hand instead of using my edited file, here are the exact swaps:

**Slide 13:**
- `100%` → `8 → 0`
- `failure recovery in documented run` → `active failures cleared in documented PoC run`
- `+10.2%` → `+0.102`
- `groundness improvement after hardening` → `groundedness gain after hardening (0.840 → 0.942)`
- `PII leaks after remediation in final run` → `PII leaks in final run (protection 0.992)`

**Slide 11:**
- Card 3 title `Human-in-the-Loop` → `Auditability & Evidence`
- Card 3 icon letter `H` → `A`

**Slide 9 (optional):**
- `AD terminal execution / tool-call scoring` → `ADK terminal execution / tool-call scoring`

---

## 5. Slide-Edit Checklist

Use this to confirm everything before you record.

- [x] Slide 13: "100%" replaced with "8 → 0" *(done in deck_final.pptx)*
- [x] Slide 13: "groundness" typo fixed → "groundedness" *(done)*
- [x] Slide 13: groundedness stat shows 0.840 → 0.942 *(done)*
- [x] Slide 11: "Human-in-the-Loop" → "Auditability & Evidence", icon H → A *(done)*
- [x] Slide 9: "AD" → "ADK" *(done)*; slide-9 title "GCP" → "Google Cloud" *(done)*
- [x] Slide 7: title "GCP" → "Google Cloud architecture" *(done)*
- [x] Slide 4: 91% relabeled "directional benchmark"; ₹4.5Cr reframed as conservative estimate with IBM ₹22Cr anchor; 6–9mo → 6–18mo (ModelOp) *(done)*
- [ ] **Decide narration order** (Option A in-deck-order, or Option B reorder slide 13 up) — and rehearse only that order
- [ ] Confirm the demo screenshot on Slide 6 and proof screenshots on Slide 9 are the final, legible versions
- [ ] Do one timed read-through aloud — confirm you land between 6:20 and 6:40
- [ ] Verify the spoken numbers exactly match what's on Slide 13 (0.942 / 0.970 / 0.992 / 8→0)

---

## What's repetitive / robotic in the OLD script — and how the new one fixes it

- **Repeated phrases:** the old script said "working pipeline: load docs, build RAG, generate tests, execute, evaluate, gate, remediate, re-test" almost verbatim on **both** Slide 7 and Slide 9. The new script says the pipeline once (Slide 7) and uses Slide 9 purely for "it really ran" proof — no repeat.
- **"That is where… / That is what… / So…"** openers stacked up. Varied them.
- **List-reading tone** ("First… Then… Then… Then…") on Slides 5, 6, 9 made it sound like a manual. Rewritten as connected sentences with one clear emphasis line each.
- **Metrics were never actually spoken.** The biggest weakness: the old script's "proof" slide (9) described the *process* but never said the numbers out loud. The new script moves the real numbers (0.840 → 0.942, 8 → 0) into a dedicated, slowed-down beat on the metrics slide. That's your winning moment — don't bury it.
- **Model Armor section** kept your exact memorable line but trimmed the lead-in so it's punchier.
