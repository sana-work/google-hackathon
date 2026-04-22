# Agentic AI Interviewer Pack (45 Minutes)

## Working scenario for the whole interview

Design an **enterprise Agentic AI assistant for operations teams**.

The system should:
- answer questions from internal docs and tickets
- use tools like:
  - knowledge search
  - SQL/query tool
  - ticketing API
  - calendar/task API
  - email/slack notification tool
- support multi-step tasks like:
  - investigate an incident
  - summarize root cause
  - create/update a ticket
  - notify the right owner
  - escalate to a human when needed
- be production-safe:
  - bounded autonomy
  - audit logs
  - access control
  - retries
  - failure handling
  - observability

Use this same scenario for all questions so you can keep saying:

**“In the agentic system you designed in Question 1…”**

---

## 45-minute interview plan

| Time | Section | Goal |
|---|---:|---|
| 0–5 min | Warm-up | Test whether they understand what an agent actually is |
| 5–18 min | Core architecture | Design the system, state, tools, boundaries |
| 18–30 min | Hands-on scenarios | Debugging, failure handling, tracing, guardrails |
| 30–40 min | Knowledge validation | Agent concepts, evaluation, memory, rollback |
| 40–45 min | Closing | Final judgment, trade-offs, candidate questions |

---

# Final Agentic AI interviewer pack

## Core questions to use in the 45-minute interview

| Q# | Exact question | What good answers must include | Red flags | Score |
|---|---|---|---|---|
| 1 | “Design a production Agentic AI system for operations teams. It should answer from internal docs, use tools to search tickets and update systems, and complete multi-step tasks like incident triage, summary generation, and owner notification. Walk me through the architecture.” | Clear layered architecture: entry/API layer, planner/router, tool layer, state store, memory layer, policy/guardrail layer, observability/tracing, human-in-loop. Should explain single-agent vs supervisor-worker or graph/state machine and why. | “Use LangGraph/CrewAI” with no architecture, no state design, no boundaries, no production controls. | /5 |
| 2 | “In the system you just designed, what state would you carry from step to step, where would you store it, and what is the difference between state and memory?” | Structured state object: task goal, step history, tool outputs, current plan, retries, budget, auth context, pending approvals. Memory should be separated from run-state. Should mention short-term vs long-term memory and contamination risks. | Vague “conversation history,” no distinction between memory and state, no storage model. | /5 |
| 3 | “What tools would you expose to the agent, and what would a good tool interface look like?” | Tool schemas, strict inputs/outputs, explicit errors, auth boundaries, idempotency, side-effect awareness, permission checks. Should explain read-only vs action tools. | Treats tools as plain text functions, no schemas, no error handling, no permission boundary. | /5 |
| 4 | “When should the agent answer directly, when should it call one tool, and when should it plan a multi-step workflow?” | Decision logic: direct answer for grounded/simple cases, single tool for exact data fetch/action, multi-step only when decomposition is necessary. Strong answer mentions cost/latency/control trade-offs. | Uses agents for everything, no routing logic, no cost awareness. | /5 |
| 5 | “How would you stop the agent from looping, repeating tools, or taking unsafe actions?” | Max steps, duplicate-action detection, retry caps, tool cooldowns, budget limits, state machine checkpoints, approval gates, policy checks, safe termination reasons. | Only says “set max iterations,” no action safety model. | /5 |
| 6 | “A failed run happened: the agent searched docs, queried a ticket, drafted a summary, then notified the wrong team. How would you debug it?” | Step-by-step trace review: state transitions, tool choice, tool params, retrieved evidence, model outputs, routing decisions, policy decisions, final action reason. Should isolate which stage failed. | “Prompt issue” without trace analysis, no root-cause method. | /5 |
| 7 | “How would you evaluate this agentic system before and after production?” | Offline and online eval. Metrics for task completion, tool correctness, plan efficiency, unnecessary steps, latency, cost, human escalation, rollback rate, policy violations. | Only answer-quality metrics, no workflow metrics, no live monitoring. | /5 |
| 8 | “What should be deterministic in this system, and what should remain model-driven?” | Deterministic: auth, permissions, budget ceilings, action approval, tool allow-lists, escalation rules, audit logs. Model-driven: summarization, reasoning over evidence, candidate planning, drafting. | Lets model decide permissions or final unsafe actions. | /5 |
| 9 | “How would you put a human in the loop without breaking the workflow?” | Explicit approval checkpoints, escalation states, resumable workflow, preserved context, minimal human burden, audit trail of human overrides. | Human review as ad hoc manual step, no state resumption. | /5 |
| 10 | “Suppose the same task produces different plans on different runs. When is that acceptable, and when is it not?” | Wording variation may be okay; action choice, ticket update, escalation path, cost, or final decision variation often not okay. Should mention temperature, plan templates, deterministic routing, approval for high-risk actions. | “LLMs are non-deterministic, so fine.” | /5 |
| 11 | “How would you design observability and tracing for this agentic system?” | Run ID, task ID, state snapshots, prompt/model version, chosen action, tool inputs/outputs, retries, latency by step, token/cost usage, termination reason, policy decisions. | Only API logs, no per-step trace, no tool visibility. | /5 |
| 12 | “Tell me one design choice you would deliberately make less clever or less autonomous in this system, and why.” | Mature trade-off: reduce autonomy, more deterministic routing, human approval, smaller scope, stricter tools, less memory, fewer agents. Must explain trade-off clearly. | Generic “be careful,” no specific subsystem or trade-off. | /5 |

---

# Detailed interviewer notes for each core question

## Q1. Architecture design

**Exact question**  
“Design a production Agentic AI system for operations teams. It should answer from internal docs, use tools to search tickets and update systems, and complete multi-step tasks like incident triage, summary generation, and owner notification. Walk me through the architecture.”

**What this tests**  
Real system design, whether the candidate understands that agents are more than prompt chains.

**Strong answer should include**
- Entry/API layer
- Auth and user context injection
- Query/task classifier
- Planner/router or state machine
- Tool execution layer
- State store
- Optional memory store
- Policy/guardrail layer
- Human approval node
- Observability/tracing
- Async workers/queue for long tasks
- Fallback path

**Best sign**  
They say something like:

> “I would not start with multi-agent by default. I’d start with a bounded agent workflow or graph/state machine, and only split roles if one agent becomes too overloaded or hard to evaluate.”

**Red flags**
- Immediately says “use AutoGen/CrewAI/LangGraph” and stops there
- No mention of state
- No mention of action boundaries
- No mention of permissions or approvals

**Good follow-up**  
“Would you start with single-agent or multi-agent, and why?”

---

## Q2. State and memory

**Exact question**  
“In the system you just designed, what state would you carry from step to step, where would you store it, and what is the difference between state and memory?”

**Strong answer should include**

### Run-state
- task ID
- user intent / goal
- current step
- prior steps
- tool outputs
- pending actions
- retry count
- budget / step count
- approval status
- auth scope

### Memory
- persistent user/team preferences
- prior resolved incidents
- historical patterns
- reusable summaries

### Storage
- state store: Redis / workflow engine / DB
- memory store: vector DB / relational DB / feature store depending use case

### Key distinction
- **State** = current run context needed to continue execution safely
- **Memory** = longer-lived information that may influence future runs

**Red flags**
- Uses memory and state interchangeably
- Wants to stuff everything into conversation history
- No mention of contamination or stale memory

**Good follow-up**  
“What would you never persist in long-term memory?”

---

## Q3. Tool design

**Exact question**  
“What tools would you expose to the agent, and what would a good tool interface look like?”

**Strong answer should include**

### Example tools
- `search_knowledge_base(query, filters)`
- `get_ticket(ticket_id)`
- `update_ticket(ticket_id, fields)`
- `get_incident_history(service_id)`
- `notify_owner(user_id, message)`
- `create_followup_task(payload)`

### Good tool interface
- strict JSON schema
- typed arguments
- explicit output structure
- explicit error states
- bounded scope
- auth and permission checks
- idempotency for write actions
- clear side effects

**Red flags**
- Free-text tool invocation
- No schema
- Agent can call destructive tools without approval
- No distinction between read and write tools

**Good follow-up**  
“Which of those tools would require human approval before execution?”

---

## Q4. Direct answer vs one tool vs multi-step plan

**Exact question**  
“When should the agent answer directly, when should it call one tool, and when should it plan a multi-step workflow?”

**Strong answer should include**
- **Direct answer**
  - when retrieved evidence is enough
  - no side effects needed
  - low ambiguity
- **One tool**
  - exact data needed
  - single lookup/action needed
- **Multi-step plan**
  - task needs decomposition
  - multiple dependencies
  - evidence + action + notification chain

**Red flags**
- Multi-step for every task
- No cost or latency trade-off
- No threshold for escalation

**Good follow-up**  
“What would your router look at before deciding to trigger a full plan?”

---

## Q5. Loop prevention and unsafe action control

**Exact question**  
“How would you stop the agent from looping, repeating tools, or taking unsafe actions?”

**Strong answer should include**
- step cap
- retry cap
- duplicate tool-call detection
- tool cooldown / dedupe
- budget limit
- action allow-list
- human approval for side effects
- stop conditions
- safe failure states
- termination reasons logged

**Red flags**
- Only “max iterations”
- No distinction between harmless repetition and dangerous repeated writes
- No approval gate

**Good follow-up**  
“How would you detect the agent is stuck, not just still working?”

---

## Q6. Debug a failed run

**Exact question**  
“A failed run happened: the agent searched docs, queried a ticket, drafted a summary, then notified the wrong team. How would you debug it?”

**Strong answer should include**
- inspect trace per step
- compare user goal vs chosen plan
- inspect retrieval evidence
- inspect tool selection
- inspect tool arguments
- inspect summary generation
- inspect notification routing decision
- inspect policy layer
- determine earliest wrong step
- decide whether failure is:
  - planning error
  - routing error
  - tool-param error
  - state corruption
  - bad retrieved evidence
  - approval/policy miss

**Red flags**
- “Tune the prompt”
- No root-cause framework
- No interest in step-level trace

**Good follow-up**  
“What exact trace fields would help you isolate whether the wrong team came from the model or from bad CRM/ticket data?”

---

## Q7. Evaluation

**Exact question**  
“How would you evaluate this agentic system before and after production?”

**Strong answer should include**

### Offline
- task completion
- plan correctness
- tool selection correctness
- tool parameter correctness
- unnecessary steps
- refusal/escalation correctness
- policy compliance
- side-effect safety

### Online
- task success rate
- escalation rate
- rollback/error rate
- step count
- latency
- cost
- user satisfaction
- retry rate
- action approval acceptance/rejection rates

**Red flags**
- Only BLEU/ROUGE or answer correctness
- No workflow metrics
- No online monitoring

**Good follow-up**  
“How would you tell if the agent is technically successful but economically inefficient?”

---

## Q8. Deterministic vs model-driven

**Exact question**  
“What should be deterministic in this system, and what should remain model-driven?”

**Strong answer should include**

### Deterministic
- permissions
- tool allow-lists
- auth
- approval rules
- budget ceilings
- workflow state transitions for risky actions
- policy checks
- audit logging

### Model-driven
- summarization
- evidence synthesis
- candidate plan generation
- explanation drafting
- low-risk prioritization suggestions

**Red flags**
- Model decides whether to send external notifications without checks
- Model decides who can access data
- Model allowed to bypass policy

**Good follow-up**  
“What is one action you would never let the model take without a rule-based gate?”

---

## Q9. Human-in-loop design

**Exact question**  
“How would you put a human in the loop without breaking the workflow?”

**Strong answer should include**
- approval state in workflow
- suspend/resume execution
- full context packet for reviewer
- minimal reviewer burden
- human override logging
- clear resume behavior after approval/rejection
- escalation thresholds

**Red flags**
- “Send it to a human”
- No resumable state
- No audit trail

**Good follow-up**  
“What data would you present to the reviewer so they can approve in under 30 seconds?”

---

## Q10. Variability across runs

**Exact question**  
“Suppose the same task produces different plans on different runs. When is that acceptable, and when is it not?”

**Strong answer should include**
- acceptable:
  - small wording variation
  - equivalent low-risk internal reasoning
- not acceptable:
  - different tools chosen for same high-risk task
  - different update actions
  - different notified owner
  - different escalation result
  - large cost/latency drift

### Controls
- fixed prompts
- lower temperature
- plan templates
- deterministic routers
- approval for high-risk actions
- compare plan signatures

**Red flags**
- Treats all variability as acceptable
- No plan normalization concept

**Good follow-up**  
“How would you compare two plans programmatically?”

---

## Q11. Observability and tracing

**Exact question**  
“How would you design observability and tracing for this agentic system?”

**Strong answer should include**
- run ID
- parent-child step IDs
- user/task ID
- state snapshot or diff
- prompt version
- model version
- action selected
- tool inputs
- tool outputs
- errors
- retries
- cost/tokens
- latency per step
- final termination reason
- policy decisions
- approval decisions

**Red flags**
- Only HTTP logs
- No step-level trace
- No tool I/O visibility

**Good follow-up**  
“What would you expose in internal debugging UI versus what would stay only in backend logs?”

---

## Q12. Deliberately less autonomous design choice

**Exact question**  
“Tell me one design choice you would deliberately make less clever or less autonomous in this system, and why.”

**Strong answer should include**  
Concrete examples:
- no multi-agent until needed
- human approval on all write actions
- no long-term memory initially
- planner only for certain task classes
- smaller tool set first
- no recursive self-reflection loops in production
- hard-coded escalation routes before dynamic routing

**Red flags**
- Generic answer
- No subsystem named
- No trade-off explained

**Good follow-up**  
“What metric would worsen because of that decision, and why would you accept it?”

---

# Extra knowledge-based questions for Agentic AI

Use 4–6 of these if time allows, or swap them into the core set depending on candidate level.

| Q# | Exact question | What good answers must include | Red flags | Score |
|---|---|---|---|---|
| 13 | “What is the difference between planning, routing, and orchestration?” | Planning = deciding sequence of actions; routing = choosing path/tool/agent; orchestration = executing steps, state, retries, dependencies. | Treats them as the same thing. | /5 |
| 14 | “What is the difference between autonomy and bounded autonomy?” | Dynamic decision-making within strict limits: tools, budgets, approvals, policies, step count. | Thinks autonomy means full freedom. | /5 |
| 15 | “Why do many agent demos fail in production?” | Happy-path only, no state discipline, weak tools, no eval, no tracing, no failure recovery, no cost control. | Blames only model quality. | /5 |
| 16 | “When is multi-agent architecture justified, and when is it overkill?” | Justified when roles are truly distinct; overkill when router/state machine is enough. | Multi-agent is always better. | /5 |
| 17 | “How would you protect an agent from prompt injection through retrieved text or tool outputs?” | Separate data from instructions, sanitize tool output, schema validation, trust boundaries, no external override of system/tool policy. | Only says ‘use a better prompt’. | /5 |
| 18 | “What is the difference between failure recovery and rollback in agentic systems?” | Recovery = continue safely after error; rollback = compensate/undo completed actions. | Uses both as synonyms. | /5 |
| 19 | “How would you version an agentic system?” | Version prompts, tools, tool schemas, routing logic, policies, workflow graph, models. | Versions only the model. | /5 |
| 20 | “What logs are essential for agent tracing?” | Run ID, step ID, action, tool I/O, prompt/model versions, retry reason, termination reason, cost, policy decisions. | Only API logs. | /5 |

---

# Recommended 45-minute version to actually run

## Option A: Best balanced 45-minute set

Ask these 8 main questions:
1. Q1 Architecture
2. Q2 State vs memory
3. Q3 Tool interfaces
4. Q4 Direct answer vs one tool vs plan
5. Q5 Loop prevention / unsafe actions
6. Q6 Debug failed run
7. Q7 Evaluation
8. Q11 Observability and tracing

Then close with:
9. Q12 Deliberately less autonomous design choice

This set gives you:
- architecture
- hands-on system thinking
- production realism
- agent-specific knowledge

---

# Suggested timing by question

| Question | Time |
|---|---:|
| Q1 | 6 min |
| Q2 | 4 min |
| Q3 | 4 min |
| Q4 | 4 min |
| Q5 | 4 min |
| Q6 | 6 min |
| Q7 | 5 min |
| Q11 | 5 min |
| Q12 | 3 min |
| Wrap-up | 4 min |

Total: **45 minutes**

---

# Fast scoring summary

At the end, rate the candidate across these 6 dimensions:

| Dimension | Score |
|---|---:|
| Agent architecture design | /5 |
| Tool and state design | /5 |
| Production reliability | /5 |
| Guardrails and safety | /5 |
| Evaluation and observability | /5 |
| Practical judgment / maturity | /5 |

### Strong hire signal
- can explain **when not to use agents**
- can define **state, tools, and boundaries clearly**
- thinks in **traces, retries, approvals, and failures**
- understands **cost/latency/observability**
- does not oversell autonomy

### Weak signal
- treats agents like magic
- only talks about prompts/frameworks
- no clear state model
- no tool discipline
- no plan for failures or tracing
