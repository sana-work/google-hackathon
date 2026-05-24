# GUARDRAIL FACTORY — TELEPROMPTER SCRIPT
### Read straight down. Each line = one breath. [PAUSE] = beat. ▸ = click to next slide.
### Target ~6:40. Don't rush the bold lines — let them land.

---

## ▸ SLIDE 1 — COVER

Hi everyone.

So we've all seen how fast GenAI assistants
are going from prototype to production these days.

The catch is —

a model that looks brilliant in a demo
can quietly start behaving differently

the moment you tweak a prompt,
swap a model version, [PAUSE]
or refresh a document.

That's exactly the tension behind today's idea:

**GenAI Guardrail Factory.**

---

## ▸ SLIDE 2 — AGENDA

In the next few minutes I'll walk you through

the problem,
the solution,
a live demo,
the architecture on Google Cloud,

and the proof that it actually runs.

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

We built this on the Build with Vertex AI track,
using Google ADK.

And the reason is right here:

enterprise GenAI needs a repeatable safety release gate
before production —
not one-time manual testing.

Gemini can generate adversarial tests and diagnose failures,
and ADK lets us run deterministic, tool-based checks.

So the question we keep asking — [PAUSE]
"Can this app answer?" —
turns out to be the wrong one.

**The real question is:
can we prove it's safe enough to release?**

---

## ▸ SLIDE 4 — THE PROBLEM

Today, most teams answer that question by hand.

They try a few sample prompts,
ask an expert to eyeball the responses,
run a security check or two,

and then someone makes a judgment call.

That's fine for a controlled demo. [PAUSE]
Production is a different world.

In production, nobody follows your script.

People ask edge-case questions.
They probe for sensitive data.
They try to override instructions.

They'll ask the assistant to approve something
it has no authority to approve.

And every so often,
the model answers with total confidence —
while being completely ungrounded in your actual documents.

That opens four doors you can't leave open: [PAUSE]

hallucination,
PII leakage,
jailbreak or role-override,
and policy-boundary violations.

And this isn't just a developer problem.

When one of those slips through,
it lands on compliance leaders,
risk and security teams,
CISOs,

and the business owner whose name is on the release.

In BFSI, that's not theoretical —
governance and auditability are mandatory.

"It worked when we tested it"
is not an audit trail.

The hard part is that the manual approach
simply doesn't scale.

**Standing up a safety framework by hand
takes six to nine months —**

and then every prompt change, model upgrade,
or document refresh
forces you to do it all over again.

So what enterprises are missing
isn't another assistant.

It's a release gate —

something that gives a clear, repeatable verdict:

this app is safe to move forward,
or this release is blocked.

---

## ▸ SLIDE 5 — OUR SOLUTION

That's what GenAI Guardrail Factory is:

a pre-production safety release gate
for enterprise GenAI applications.

For this proof-of-concept,
my target app was an HR Policy assistant,
running on synthetic HR documents.

But I want to be clear — [PAUSE]

**the HR assistant is just the test vehicle.
The product is the gate around it.**

That gate is designed to wrap any GenAI app.

Think of it as a safety inspection line,
before a vehicle is allowed onto the road.

The app gets submitted for evaluation.

Gemini then generates adversarial test cases —
not friendly demo prompts,
but attacks built to find the cracks.

Each response is scored by dedicated safety tools —
for groundedness, toxicity, and PII risk.

And a deterministic release gate decides: [PAUSE]
block, or approve.

Here's what makes it more than a scanner.

If the app fails,
we don't stop at a red light.

Gemini diagnoses why it failed,
hardens the prompt to close that gap,
and re-runs the exact same test suite.

So the full lifecycle is: [PAUSE]
**block, diagnose, harden, re-test, approve.**

It doesn't just flag risk —
it drives a measurable recovery.

---

## ▸ SLIDE 6 — SOLUTION IN ACTION

This is the working dashboard —
the operator's view of a real run.

A team configures the model,
the thresholds,
the policy corpus,
and the run mode.

They submit the target app,
and Gemini fans out adversarial tests across categories —

hallucination,
PII extraction,
jailbreak attempts,
toxicity,
and policy-risk scenarios.

In HR terms, that's checking
whether the assistant leaks an employee's details,
obeys a malicious instruction,
or hands out an approval
it was never authorized to give.

Google ADK then routes every response
to the right tool.

The groundedness checker confirms the answer
is actually backed by source documents.

The PII scanner hunts for sensitive identifiers.

The toxicity judge checks tone and safety.

Cross a threshold the wrong way,
and deployment is blocked —
right here on screen.

From there the system moves into auto-remediation,
hardens the prompt,
re-runs,

and only flips to approved
once recovery is proven.

So this screen isn't a report. [PAUSE]

**It's a live safety workflow
you can watch make a decision.**

---

## ▸ SLIDE 7 — ARCHITECTURE

Here's how it all runs end-to-end
on Google Cloud.

On the left is the target app —
our HR Policy assistant.

Its requests flow into a FastAPI Orchestrator,
which controls the run,
manages thresholds,
and routes results.

At the core sits the Google ADK LlmAgent,
powered by Gemini 2.5 Flash.

This is the brain
that generates the adversarial tests,
diagnoses failures,
and proposes the prompt hardening.

But — and this is the crucial design choice — [PAUSE]

the deploy decision is not left
to a free-form model answer.

The agent calls dedicated tools:
the groundedness checker,
the PII scanner,
the toxicity judge.

Grounding is anchored in ChromaDB,
against the synthetic HR documents —

so every answer is measured
against real source content.

Those scores feed the deterministic release gate,

which applies the policy:
groundedness, toxicity, and PII thresholds,
a category floor,
and a zero-critical-failures rule.

For the PoC, run history lives in a SQLite RunStore,
and Cloud Run makes the service deployable.

At enterprise scale,
that same evidence flows into BigQuery and Looker
for governance dashboards.

So the pipeline reads cleanly: [PAUSE]

load documents,
build the RAG context,
generate tests,
execute,
evaluate,
gate,
remediate,
re-test.

---

## ▸ SLIDE 8 — UNDER THE HOOD

One quick point on why this design holds up.

It's deliberately hybrid.

Gemini does the semantic work —
inventing attacks,
spotting failure patterns,
suggesting fixes.

But the final verdict is deterministic,
driven by fixed thresholds.

That split matters,

because governance needs the same inputs
to produce the same decision every time —

consistent, traceable, audit-ready.

**So the novelty isn't "AI evaluating AI." [PAUSE]
It's AI evaluating, explaining, hardening, and verifying AI —
inside one repeatable release process.**

---

## ▸ SLIDE 9 — PROOF OF EXECUTION

And this actually ran —
end-to-end on Google Cloud.

These screenshots walk the real path:

documents loaded and indexed,
the RAG context built,
Gemini generating adversarial prompts,
the ADK agent calling each safety tool,
the gate applying thresholds,

a failure triggering hardened guidance from Gemini,
and a re-run to confirm recovery.

**Build, deploy, validate — [PAUSE]
not a slideware mockup,
a working pipeline.**

---

## ▸ SLIDE 13 — THE PROOF METRICS
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

## ▸ SLIDE 10 — MODEL ARMOR COMPARISON

The natural question:
how is this different from Google Model Armor?

Model Armor is runtime protection.

It guards live prompts, responses,
documents, and agent interactions —

against things like prompt injection,
jailbreaks,
data leakage,
and harmful content —

while the app is in use.

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

## ▸ SLIDES 11 & 12 — SECURITY, SCALE & VALUE
### (Keep tight. Fold into the close if you're near 6:50.)

Underneath, four responsible-AI guardrails hold the line:

data privacy,
through multi-pattern PII detection;

grounding,
through source-document checks;

auditability —
every score, threshold, verdict, and timestamp
stored as evidence;

and domain boundaries,
that reject role overrides
and unauthorized approvals.

And because the architecture is modular
and runs on Cloud Run,

the same gate extends well past HR —

into BFSI assistants,
compliance copilots,
support bots,
and regulated RAG workflows.

For TCS, that's a reusable
GenAI Safety-as-a-Service accelerator.

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
