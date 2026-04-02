# Decision DNA — Multi-Agent Setup Guide (Gemini Enterprise)

> **Environment:** Gemini Enterprise Plus at `vertexaisearch.cloud.google.com`
> **Grounding Method:** Google Drive (Drive connector is enabled)

---

## Step 1 — Upload Enterprise Memory to Google Drive

Since the environment uses **Drive as the knowledge connector** (not a separate Data Store), upload all enterprise documents to a dedicated Drive folder.

1. Open **Google Drive**.
2. Create a new folder called **`Decision DNA - Enterprise Memory`**.
3. Upload **all 16 files** from your local `Data_Store_Docs/` folder into this Drive folder:

   | # | File | Purpose |
   |---|------|---------|
   | 1 | `Global_Security_Policy_v4.txt` | Security rules (data residency, encryption, IAM, network, zero trust) |
   | 2 | `GDPR_Data_Processing_Addendum.txt` | EU compliance (data locations, consent, profiling, sub-processors) |
   | 3 | `Payment_API_SLA.txt` | SLA targets (99.99% uptime, 400ms P95, error rate budget, change freezes) |
   | 4 | `ADR_042_Database_Selection.txt` | Firestore > Cloud SQL decision (with benchmarks and exception criteria) |
   | 5 | `ADR_018_Event_Driven_Architecture.txt` | Pub/Sub > REST/gRPC decision |
   | 6 | `ADR_031_API_Gateway_Standard.txt` | **[NEW]** API Gateway mandate for all external APIs |
   | 7 | `ADR_055_Cloud_Cost_Governance.txt` | **[NEW]** FinOps standards (labels, instance governance, cost reviews) |
   | 8 | `ARB_Meeting_47_Minutes.txt` | Meeting minutes reaffirming past ADRs |
   | 9 | `Incident_Response_Runbook.txt` | Severity levels, escalation rules |
   | 10 | `Vendor_Contract_Acme_Cloud.txt` | Vendor obligations, data sovereignty, SLA penalties |
   | 11 | `Engineering_Coding_Standards.txt` | API, security, logging, error handling |
   | 12 | `Security_Review_Checklist.txt` | Pre-deployment security checklist |
   | 13 | `Post_Mortem_Payment_Outage_2024_07.txt` | **[NEW]** Cascading failure post-mortem (reinforces ADR-018) |
   | 14 | `Post_Mortem_PII_Leak_2025_01.txt` | **[NEW]** PII logging incident (reinforces Coding Standards 3.3) |
   | 15 | `Cloud_Architecture_Standards.txt` | **[NEW]** Approved regions, GKE, VPC, tech stack |
   | 16 | `Data_Classification_Policy.txt` | **[NEW]** 4-tier data classification with handling rules |

4. Make sure the **Drive connector is enabled** (you already have it ON in your settings as shown in the connector toggle panel).

---

## Step 2 — Create Agent 1: Conflict Sentinel

1. In the sidebar, click **+ New agent**.
2. **Name:** `Conflict Sentinel`
3. Open **`Agent_Instructions.txt`** from your local machine → **Copy entire contents**.
4. Paste into the agent's **Instructions** box.
5. In the agent settings, ensure:
   - **Drive** connector is enabled (so it can search your uploaded documents)
   - Optionally mention in the instructions to reference the "Decision DNA - Enterprise Memory" folder
6. **Save** the agent.

---

## Step 3 — Create Agent 2: Code Review Judge (CRJ)

1. Click **+ New agent** again.
2. **Name:** `Code Review Judge`
3. Open **`Agent_CRJ_Instructions.txt`** → **Copy entire contents**.
4. Paste into the agent's **Instructions** box.
5. Ensure **Drive** connector is enabled.
6. **Save** the agent.

---

## Step 4 — Create the Orchestrator (Main Agent)

1. Click **+ New agent** again.
2. **Name:** `Decision DNA`
3. Open **`Agent_Orchestrator_Instructions.txt`** → **Copy entire contents**.
4. Paste into the agent's **Instructions** box.
5. Ensure **Drive** connector is enabled.
6. **Save** the agent.

> **Alternative (Simpler):** If you find that separate sub-agents can't call each other in this interface, you can use a **single combined agent** instead. I have also created **`Agent_Combined_Instructions.txt`** which merges all capabilities into one powerful agent. See Step 4b below.

### Step 4b — Single Combined Agent (If Multi-Agent Routing Isn't Available)

1. Click **+ New agent**.
2. **Name:** `Decision DNA`
3. Open **`Agent_Combined_Instructions.txt`** → Copy + Paste.
4. Ensure **Drive** connector is enabled.
5. This single agent handles ALL capabilities: Conflict Sentinel, Code Review Judge, Ask Why, Impact Analysis, Compliance Scorecard, and Onboarding Brief.

---

## Step 5 — Smoke Test

Open the agent (whichever you created) and type:

```text
Review this draft:
"We will keep audit logs for only 30 days to save storage costs."
```

✅ **Expected:** Flags a violation citing `Global_Security_Policy_v4.txt` (90-day minimum).

---

## Step 6 — Configure Scheduled Compliance Scan (Optional but Impressive)

This sets up an automated weekly compliance sweep — the "production readiness" feature.

1. Open the **Decision DNA** agent (or Combined agent) in the Agent Designer.
2. Click the **Schedule** tab.
3. Click **+ Add schedule**.
4. Configure:
   - **Frequency:** Weekly (Every Monday)
   - **Time:** 09:00 AM
5. In the **Prompt** field, paste:

```text
Run a weekly enterprise compliance health check. Scan all documents in the Decision DNA Enterprise Memory folder and generate a Compliance Status Report covering:
1. Review all internal policies and identify any that reference outdated standards, expired certifications, or past review dates that have lapsed.
2. Check for cross-document consistency: Are any policies contradicting each other?
3. Review vendor contracts for upcoming expiry dates or certification renewal deadlines within the next 90 days.
4. Identify any compliance gaps where a regulation or policy mandate exists but no corresponding internal standard is documented.
Format as: Critical Issues, Warnings, Upcoming Deadlines, Recommendations.
```

6. Click **Save**. The schedule becomes active after you click **Update** on the agent.

> **Demo Tip:** During a live demo, show the Schedule tab configuration to demonstrate production readiness, then manually run the prompt to show the automated output.

## Step 7 — Run the Full Demo

Open **`Demo_Script.md`** and run the 9 scenarios:

| Demo | Tests | Expected |
|------|-------|----------|
| 1 — PRD Review | Conflict Sentinel | 5-6 policy/compliance violations |
| 2 — Code Review | Code Review Judge | Security + architecture findings |
| 3 — Ask Why | Decision Tracing | Cited ADR + meeting reaffirmation |
| 4 — Safe Draft | Precision | Clean pass, no false alarms |
| 5 — Combined | Both agents | Document + code review together |
| 6 — Institutional Memory | Post-Mortem Intelligence | Cites past outage when sync REST proposed |
| 7 — Terraform Review | IaC Compliance | Cloud, cost, security infrastructure findings |
| 8 — Onboarding Brief | Knowledge Synthesis | Multi-document briefing for new team member |
| 9 — Scheduled Scan | Automated Compliance | Weekly compliance report with proactive alerts |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Agent gives generic answers | It's not finding Drive docs. Make sure the Drive connector toggle is ON. Also try mentioning "search the Decision DNA Enterprise Memory folder in Drive" in your prompt. |
| Agent says it can't access files | The files may not be indexed yet. Wait a few minutes after upload. |
| Can't link sub-agents together | Use the **Combined Agent** approach (Step 4b) — one agent, all capabilities. |
| Agent doesn't cite post-mortems | Ensure the two Post-Mortem files are uploaded. They are critical for Demo 6. |

---

## File Inventory

```text
Idea 4 Vertex AI Setup/
├── Setup_Guide.md                              ← This file (START HERE)
├── Agent_Orchestrator_Instructions.txt         ← Orchestrator (multi-agent routing)
├── Agent_Instructions.txt                      ← Conflict Sentinel
├── Agent_CRJ_Instructions.txt                  ← Code Review Judge
├── Agent_Combined_Instructions.txt             ← All-in-one single agent (fallback)
├── Demo_Script.md                              ← 8 demo scenarios
└── Data_Store_Docs/ (16 files)                 ← Upload ALL to Google Drive
    ├── ADR_018_Event_Driven_Architecture.txt
    ├── ADR_031_API_Gateway_Standard.txt         [NEW]
    ├── ADR_042_Database_Selection.txt
    ├── ADR_055_Cloud_Cost_Governance.txt         [NEW]
    ├── ARB_Meeting_47_Minutes.txt
    ├── Cloud_Architecture_Standards.txt          [NEW]
    ├── Data_Classification_Policy.txt            [NEW]
    ├── Engineering_Coding_Standards.txt
    ├── GDPR_Data_Processing_Addendum.txt
    ├── Global_Security_Policy_v4.txt
    ├── Incident_Response_Runbook.txt
    ├── Payment_API_SLA.txt
    ├── Post_Mortem_Payment_Outage_2024_07.txt    [NEW]
    ├── Post_Mortem_PII_Leak_2025_01.txt          [NEW]
    ├── Security_Review_Checklist.txt
    └── Vendor_Contract_Acme_Cloud.txt
```
