# GUARDRAIL FACTORY — TELEPROMPTER SCRIPT
### Read straight down. Each line = one breath. [PAUSE] = beat. ▸ = click to next slide.
### Target ~6:05–6:15 spoken (trimmed). Don't rush the bold lines — let them land.

---

## ▸ SLIDE 1 — COVER

Hi everyone.

Welcome to GenAI Guardrail Factory —

our answer to a question
every enterprise is quietly worried about.

So we've all seen how fast GenAI assistants
are going from prototype to production these days.

The catch is —

a model that looks brilliant in a demo
can quietly start behaving differently

the moment you tweak a prompt,
swap a model version, [PAUSE]
or refresh a document.

That's exactly the tension
behind everything you're about to see.

---

## ▸ SLIDE 3 — TEAM & TRACK

And quickly about me —

I'm Sana Iqbal,
a GenAI Solution Architect
on the AI Services team in our BFSI unit.

So I spend my days where responsible AI, privacy,
and production-readiness aren't nice-to-haves —

they're the difference between a release going out,
and a release getting stopped.

So the question we keep asking — [PAUSE]
"Can this app answer?" —
turns out to be the wrong one.

**The real question is:
can we prove it's safe enough to release?**

---

## ▸ SLIDE 4 — THE PROBLEM

Today, most teams answer that by hand —
a few prompts, an expert eyeballing responses,
a security check, a judgment call.

Fine for a demo. [PAUSE]
Production is a different world.

There, nobody follows your script.
People probe for sensitive data,
override instructions,

ask the assistant to approve things
it has no authority to approve —

and sometimes it answers with total confidence,
while being completely ungrounded in your documents.

That opens four doors you can't leave open: [PAUSE]

hallucination,
PII leakage,
jailbreak or role-override,
and policy-boundary violations.

And this isn't just a developer problem —

when one slips through, it lands on
compliance, risk, the CISO,

and the business owner whose name is on the release.


**And building a safety framework takes six to nine months,**

and every prompt or model change
forces you to start over.

So what's missing isn't another assistant.

It's a release gate —
a clear, repeatable verdict:
safe to ship, or blocked.

---

## ▸ SLIDE 5 — OUR SOLUTION

That's what GenAI Guardrail Factory is:

a **CI/CD-style safety release gate**
for enterprise GenAI applications —

just as code passes automated tests before it ships,
your GenAI app must pass safety before it goes live.

My proof-of-concept wraps an HR Policy assistant —
but to be clear: [PAUSE]

**the assistant is just the test vehicle.
The product is the gate around it** —
designed to wrap any GenAI app.

Plenty of tools can scan a model.
Three things make this different:

**it's agentic** — a Google ADK agent
actively calls tools to score the app;

**it's grounded** — every check runs
against your own source documents;

**and it's enterprise-ready** —
thresholds, audit logs, Cloud Run.

But the real novelty? [PAUSE]
It doesn't stop at flagging risk —
it hardens the app and re-tests
until safety is proven.

**So this isn't AI evaluating AI.
It's AI evaluating, explaining, hardening,
and verifying AI.**

---

## ▸ SLIDE 6 — SOLUTION IN ACTION

This is the working dashboard —
the operator's view of a real run.

A team configures the model, thresholds,
and policy corpus, then submits the app —

and Gemini fans out adversarial tests:
hallucination, PII extraction,
jailbreaks, toxicity, policy-risk.

Google ADK routes every response to the right tool —
the groundedness checker,
the PII scanner,
the toxicity judge.

Cross a threshold the wrong way,
and deployment is blocked —
right here on screen.

From there it auto-remediates,
hardens the prompt, re-runs,

and only flips to approved
once recovery is proven.

So this isn't a report. [PAUSE]

**It's a live safety workflow
you can watch make a decision.**

---

## ▸ SLIDE 7 — ARCHITECTURE

Here's how it runs end-to-end
on Google Cloud.

The target app — our HR assistant —
sends requests into a FastAPI Orchestrator
that controls the run and routes results.

At the core is the Google ADK LlmAgent,
powered by Gemini 2.5 Flash —

the brain that generates the tests,
diagnoses failures,
and proposes the hardening.

But here's the crucial design choice: [PAUSE]

the deploy decision is not left
to a free-form model answer.

The agent calls dedicated tools —
groundedness, PII, toxicity —

with grounding anchored in ChromaDB
against the real source documents.

Those scores feed the deterministic release gate,

which applies the policy:
the thresholds, a category floor,
and zero critical failures.

Run history lives in a SQLite RunStore,
Cloud Run makes it deployable,

and at enterprise scale that evidence
flows into BigQuery and Looker.

So the pipeline reads cleanly: [PAUSE]

load, ground, test, evaluate,
gate, remediate, re-test.

---

## ▸ SLIDE 8 — UNDER THE HOOD

One quick point on why this holds up.

It's deliberately hybrid.
Gemini does the semantic work —
inventing attacks, spotting patterns, suggesting fixes.

But the final verdict is deterministic,
driven by fixed thresholds.

That matters, because governance needs
the same inputs to give the same decision
every time — traceable and audit-ready.

That's what turns a clever demo
into something a risk team can sign off on.

---

## ▸ SLIDE 9 — PROOF OF EXECUTION

And this actually ran —
end-to-end on Google Cloud.

These screenshots walk the real path:

a failure triggering hardened guidance from Gemini,
and a re-run to confirm recovery.

**Build, deploy, validate — [PAUSE]
not a slideware mockup,
a working pipeline.**

---

## ▸ SLIDE 10 — THE PROOF METRICS
### (Slow down. This is the moment. Let every number land.)

Here's what that run produced.

Going in,
groundedness measured **0.840** —

just under the **0.850** threshold,
with **eight active failures** on the board.

Verdict: [PAUSE]
**deployment blocked.**

Then remediation ran.

Groundedness climbed to **0.942.**
Toxicity safety reached **0.970.**
PII protection, **0.992.**

And those eight active failures? [PAUSE]

**Reduced to zero —
in the documented PoC run.**

Verdict: [PAUSE]
**approved for deployment.**

That's the whole thesis in one screen —

a release that should have been stopped,
was stopped,

then recovered to a measurable,
evidence-backed pass.

---

## ▸ SLIDE 11 — MODEL ARMOR COMPARISON

The natural question:
how is this different from Google Model Armor?

Model Armor is runtime protection.
It guards live prompts, responses,
and agent interactions —

against prompt injection, jailbreaks,
and data leakage, while the app is in use.

Guardrail Factory works one step earlier.

Put simply: [PAUSE]

**Model Armor asks,
"Is this prompt or response safe right now?"**

**Guardrail Factory asks,
"Is this whole application safe enough to release?"**

They're complementary, not competing.

**Model Armor protects the live road. [PAUSE]
Guardrail Factory decides whether the vehicle
is safe enough to get on it.**

You want both.

---

## ▸ SLIDES 12 & 13 — SECURITY, SCALE & VALUE
### (Keep tight. Fold into the close if you're near 6:50.)

Security isn't a feature in this application —
security is the application.

And because the architecture is modular
and runs on Cloud Run,

the same gate extends well past HR —

into BFSI assistants,
compliance copilots,
support bots,
and regulated RAG workflows.

For TCS, that's a reusable
**GenAI Safety-as-a-Service accelerator.**

---

## ▸ SLIDE 15 — CLOSE

So, to bring it home.

Enterprises don't just need
impressive GenAI demos.

They need GenAI they can trust in production —

and trust you can show,

backed by adversarial testing,
deterministic thresholds,
remediation,
and audit evidence.

**Good GenAI demos show capability. [PAUSE]
Guardrail Factory proves deployability.**

Thank you.
