# 📸 Idea 4 — Decision DNA: Screenshot Checklist

> **Track:** Track 1 — Intelligent Search & Gemini Enterprise
> **Platform:** Gemini Enterprise Agent Designer at `vertexaisearch.cloud.google.com`
> **Concept:** Multi-Agent Enterprise Memory System (Conflict Sentinel + Code Review Judge)

---

## REQUIRED Screenshots (Track 1 Rubric)

### 📸 1. Agent Architecture (Flow View)
**Where:** Agent Designer → Open "Decision DNA" agent → Click "Flow" tab
**What to capture:** The Agent Designer UI showing the multi-agent routing

- [ ] **Screenshot 1a:** Flow view showing the Orchestrator (Decision DNA) → sub-agents (Conflict Sentinel, Code Review Judge)
- [ ] **Screenshot 1b:** If using single combined agent, show the agent name + model selection in the main config panel

---

### 📸 2. Instructions & Guardrails
**Where:** Agent Designer → Open agent → "Instructions" tab
**What to capture:** The System Instructions panel showing security rules

- [ ] **Screenshot 2a:** Top of instructions — showing agent role, multi-agent routing logic
- [ ] **Screenshot 2b:** Security & Guardrails section — highlighting:
  - PII Prevention (never output PII, redact logs)
  - Zero Hallucination / Grounding enforcement (must cite specific documents)
  - Citation Mandatory rule
  - Human-in-the-loop disclaimer

> ⚠️ **Critical:** Rubric says *"Highlight the rules where you enforce security, prevent PII leaks, or mandate citations"*

---

### 📸 3. Data Grounding (Knowledge / Connectors)
**Where:** Agent Designer → Knowledge/Data Store tab + Google Drive

- [ ] **Screenshot 3a:** The Knowledge/Connectors panel showing **Google Drive** connector enabled
- [ ] **Screenshot 3b:** Google Drive showing the **"Decision DNA - Enterprise Memory"** folder with all 16 files visible (ADRs, policies, post-mortems, SLAs, contracts, coding standards, etc.)

---

### 📸 4. Proof of Execution (Preview Chat — Show 2-3 interactions)

Run these demos in the Preview chat and capture FULL responses:

- [ ] **Screenshot 4a — PRD Review (Conflict Sentinel):**
  > Paste Demo 1 prompt: *"Please review this draft PRD for Project Aurora..."* (the full PRD with EU data in us-west1, PostgreSQL, sync REST, 45-day logs, non-anonymized data, third-party vendor in Singapore)
  > **Capture:** The Conflict Cards showing 🔴 GDPR region violation, log retention violation, architecture violations (ADR-018, ADR-042), data minimization, vendor risk

- [ ] **Screenshot 4b — Code Review (Code Review Judge):**
  > Paste Demo 2 prompt: *"Please review this code for our new analytics service..."* (Python code with hardcoded secrets, SQL injection, PII logging)
  > **Capture:** The code review findings showing 🔴 REJECT for secrets, SQL injection, PII logging + 🟡 NEEDS CHANGE for psycopg2/Cloud SQL, sync REST

- [ ] **Screenshot 4c — Ask Why (Decision Traceability):**
  > Type: *"Why did we choose Pub/Sub over gRPC? A new hire wants to use gRPC for their service"*
  > **Capture:** The cited response referencing ADR-018, the cascading failure incident, and warning about sync proposals

- [ ] **Screenshot 4d — Institutional Memory (Post-Mortem Intelligence) [BONUS]:**
  > Paste Demo 6 prompt: *"Review this proposal: We are building a new Notifications Service using synchronous REST calls..."*
  > **Capture:** The response citing the Post-Mortem Payment Outage (July 2024) — this proves deep organizational memory beyond simple policy checking

---

### 📸 5. Scheduled Compliance Scan (BONUS — Production Readiness)
**Where:** Agent Designer → Schedule tab

- [ ] **Screenshot 5a:** The Schedule tab showing the weekly Monday 9AM compliance sweep configured

---

## Summary: 12-14 Screenshots Total

| # | Screenshot | Rubric Area | Priority |
|---|-----------|-------------|----------|
| 1a | Agent Flow View (multi-agent routing) | Agent Architecture | 🔴 MUST |
| 1b | Agent config (name + model) | Agent Architecture | 🔴 MUST |
| 2a | Instructions — top (role + routing) | Instructions & Guardrails | 🔴 MUST |
| 2b | Instructions — security/guardrails section | Instructions & Guardrails | 🔴 MUST |
| 3a | Knowledge connector (Drive enabled) | Data Grounding | 🔴 MUST |
| 3b | Drive folder with 16 enterprise docs | Data Grounding | 🔴 MUST |
| 4a | PRD Review → Conflict Cards | Proof of Execution | 🔴 MUST |
| 4b | Code Review → Security findings | Proof of Execution | 🔴 MUST |
| 4c | Ask Why → Decision traceability | Proof of Execution | 🟡 HIGH |
| 4d | Institutional Memory → Post-mortem cite | Proof of Execution | 🟡 HIGH |
| 5a | Schedule tab configuration | Production Readiness | 🟡 HIGH |

> **Pro Tips:**
> - For 4a and 4b, the responses will be LONG — scroll and take multiple screenshots to capture all Conflict Cards and findings
> - 4d (Institutional Memory) is a **differentiator** — it proves your agent doesn't just check policies but remembers past incidents. Take this screenshot!
> - Show **both** sub-agents being activated if possible (Demo 5 — Combined Review triggers both Sentinel + CRJ)
