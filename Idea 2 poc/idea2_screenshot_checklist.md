# 📸 Idea 2 — Regulatory Change Impact Radar: Screenshot Checklist

> **Track:** Track 1 — Intelligent Search & Gemini Enterprise
> **Platform:** Gemini Enterprise Agent Designer at `vertexaisearch.cloud.google.com`

---

## REQUIRED Screenshots (Track 1 Rubric)

### 📸 1. Agent Architecture (Flow View)
**Where:** Agent Designer → Open "Regulatory Radar" agent → Click "Flow" tab
**What to capture:** The Agent Designer UI showing the Main Agent and any Sub-agents (Regulatory Analyzer, Impact Mapper) in the Flow view
- [ ] **Screenshot 1a:** Flow view showing the multi-agent architecture (Orchestrator → sub-agents)
- [ ] **Screenshot 1b:** If using single combined agent, show the agent name + model selection in the main config

---

### 📸 2. Instructions & Guardrails
**Where:** Agent Designer → Open agent → "Instructions" tab
**What to capture:** The System Instructions panel showing your guardrails

- [ ] **Screenshot 2a:** Top of instructions showing the agent's role and capabilities
- [ ] **Screenshot 2b:** Bottom of instructions showing the **SECURITY & GUARDRAILS (MANDATORY)** section — highlighting:
  - PII Prevention rules
  - Zero Hallucination / Grounding enforcement  
  - Citations mandatory
  - Human-in-the-loop disclaimer

> ⚠️ **Critical:** The rubric says *"Highlight the rules where you enforce security, prevent PII leaks, or mandate citations"*

---

### 📸 3. Data Grounding (Knowledge / Connectors)
**Where:** Agent Designer → Open agent → "Knowledge" or "Data Store" tab
**What to capture:** The connected data sources

- [ ] **Screenshot 3a:** The Knowledge/Connectors panel showing **Google Drive** connector enabled
- [ ] **Screenshot 3b:** Google Drive showing the **"Regulatory Radar - Enterprise Knowledge"** folder with all 16 files visible

---

### 📸 4. Proof of Execution (Preview Chat — 2-3 interactions)
**Where:** Agent Designer → "Preview" chat panel (right side)

Run these demos and capture each response:

- [ ] **Screenshot 4a — DPDPA Impact Analysis:** 
  > Paste: *"A new DPDPA Amendment 2026 has been notified by MeitY. Key changes: 1) Maximum data retention reduced from 5 years to 3 years 2) Consent model changed from opt-out to mandatory explicit opt-in 3) Automated deletion mechanisms are now mandatory. Analyze the impact on our enterprise."*
  > **Capture:** The Impact Cards with severity ratings (🔴 Critical, 🟡 High) and the Impact Summary Dashboard

- [ ] **Screenshot 4b — Compliance Scorecard:**
  > Paste: *"Are we compliant with the SEBI Cyber Security Framework? Check our IT Security Policy, vendor contracts, and system registry."*
  > **Capture:** The Compliance Scorecard showing ✅ Compliant, ⚠️ Partial, ❌ Non-Compliant items

- [ ] **Screenshot 4c — Regulatory Landscape Brief:**
  > Paste: *"I'm a new compliance officer joining next week. What regulations, policies, and past incidents should I know about?"*
  > **Capture:** The comprehensive Regulatory Landscape Brief output

---

### 📸 5. Scheduled Compliance Scan (BONUS — Production Readiness)
**Where:** Agent Designer → Schedule tab

- [ ] **Screenshot 5a:** The Schedule tab showing the weekly Monday 9AM compliance sweep configured

---

## Summary: 12 Screenshots Total

| # | Screenshot | Rubric Area | Priority |
|---|-----------|-------------|----------|
| 1a | Agent Flow View (multi-agent) | Agent Architecture | 🔴 MUST |
| 1b | Agent config (model + name) | Agent Architecture | 🔴 MUST |
| 2a | Instructions — top section | Instructions & Guardrails | 🔴 MUST |
| 2b | Instructions — security/guardrails section | Instructions & Guardrails | 🔴 MUST |
| 3a | Knowledge connector (Drive enabled) | Data Grounding | 🔴 MUST |
| 3b | Drive folder with 16 documents | Data Grounding | 🔴 MUST |
| 4a | DPDPA Impact Analysis response | Proof of Execution | 🔴 MUST |
| 4b | SEBI Compliance Scorecard response | Proof of Execution | 🔴 MUST |
| 4c | Regulatory Landscape Brief response | Proof of Execution | 🟡 HIGH |
| 5a | Schedule tab configuration | Production Readiness | 🟡 HIGH |

> **Tip:** For screenshots 4a-4c, scroll through the FULL response to capture the Impact Cards, Dashboards, and Remediation Plans. You may need multiple screenshots per demo to capture long responses.
