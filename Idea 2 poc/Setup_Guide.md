# Regulatory Change Impact Radar — Setup Guide (Gemini Enterprise)

> **Environment:** Gemini Enterprise Plus at `vertexaisearch.cloud.google.com`
> **Grounding Method:** Google Drive (Drive connector is enabled)

---

## Step 1 — Upload Enterprise Knowledge to Google Drive

Since the environment uses **Drive as the knowledge connector**, upload all enterprise documents to a dedicated Drive folder.

1. Open **Google Drive**.
2. Create a new folder called **`Regulatory Radar - Enterprise Knowledge`**.
3. Upload **all 16 files** from your local `Data_Store_Docs/` folder into this Drive folder:

   **Regulatory Documents (5):**

   | # | File | Purpose |
   |---|------|---------|
   | 1 | `REG_DPDPA_Amendment_2026.txt` | DPDPA amendment — retention, consent, cross-border transfer |
   | 2 | `REG_RBI_Data_Localization_Circular.txt` | RBI circular — financial data must stay in India |
   | 3 | `REG_SEBI_Cyber_Security_Framework.txt` | SEBI framework — incident reporting, vulnerability mgmt, access control |
   | 4 | `REG_EU_AI_Act_Compliance_Notice.txt` | EU AI Act — risk classification, transparency, human oversight |
   | 5 | `REG_GDPR_Amendment_Cross_Border.txt` | GDPR — tighter cross-border transfer rules, enhanced TIA |

   **Internal Enterprise Policies (5):**

   | # | File | Purpose |
   |---|------|---------|
   | 6 | `POL_Data_Privacy_Policy_v3.txt` | Data privacy — retention, consent model, data handling |
   | 7 | `POL_IT_Security_Policy_v2.txt` | IT security — encryption, access control, incident response |
   | 8 | `POL_Vendor_Management_Policy.txt` | Vendor assessment, data sharing, SLA requirements |
   | 9 | `POL_Data_Retention_SOP.txt` | SOP for data retention and deletion processes |
   | 10 | `POL_AI_ML_Governance_Policy.txt` | AI/ML model governance — bias, explainability, oversight |

   **System Registry & Contracts (3):**

   | # | File | Purpose |
   |---|------|---------|
   | 11 | `SYS_Enterprise_System_Registry.txt` | 5 IT systems with data flows, locations, owners |
   | 12 | `CONTRACT_CloudVault_Storage.txt` | Cloud storage vendor — India + Singapore DR |
   | 13 | `CONTRACT_AnalyticsPro_DataProcessor.txt` | Analytics vendor — Singapore + US sub-processor |

   **Institutional Memory & Tracking (3):** **[NEW]**

   | # | File | Purpose |
   |---|------|---------|
   | 14 | `INCIDENT_Compliance_Breach_History.txt` | **[NEW]** 3 past compliance incidents (GDPR fine, RBI warning, EU AI Act advisory) |
   | 15 | `RPT_Board_Compliance_Report_Q3_2025.txt` | **[NEW]** Board compliance status baseline with gaps and risk scores |
   | 16 | `CAL_Regulatory_Compliance_Calendar.txt` | **[NEW]** 12-month regulatory deadline calendar with readiness status |

4. Make sure the **Drive connector is enabled** in your agent settings.

---

## Step 2 — Create Agent 1: Regulatory Analyzer

1. In the sidebar, click **+ New agent**.
2. **Name:** `Regulatory Analyzer`
3. Open **`Agent_Regulatory_Analyzer_Instructions.txt`** from your local machine → **Copy entire contents**.
4. Paste into the agent's **Instructions** box.
5. Ensure **Drive** connector is enabled.
6. **Save** the agent.

---

## Step 3 — Create Agent 2: Impact Mapper

1. Click **+ New agent** again.
2. **Name:** `Impact Mapper`
3. Open **`Agent_Impact_Mapper_Instructions.txt`** → **Copy entire contents**.
4. Paste into the agent's **Instructions** box.
5. Ensure **Drive** connector is enabled.
6. **Save** the agent.

---

## Step 4 — Create the Orchestrator (Main Agent)

1. Click **+ New agent** again.
2. **Name:** `Regulatory Radar`
3. Open **`Agent_Orchestrator_Instructions.txt`** → **Copy entire contents**.
4. Paste into the agent's **Instructions** box.
5. Ensure **Drive** connector is enabled.
6. **Save** the agent.

> **Alternative (Simpler):** If separate sub-agents can't call each other in this interface, use a **single combined agent** instead. See Step 4b below.

### Step 4b — Single Combined Agent (If Multi-Agent Routing Isn't Available)

1. Click **+ New agent**.
2. **Name:** `Regulatory Radar`
3. Open **`Agent_Combined_Instructions.txt`** → Copy + Paste.
4. Ensure **Drive** connector is enabled.
5. This single agent handles ALL 7 capabilities: Regulatory Analysis, Impact Mapping, Compliance Checks, What-If Analysis, Deadline Tracking, Audit Readiness, and Regulatory Landscape Brief.

---

## Step 5 — Configure Starter Prompts

In the agent's **Personalization** section, add these starter prompts:

```text
A new DPDPA Amendment reduces data retention to 3 years and requires opt-in consent. What is the impact on our enterprise?
```

```text
Are we compliant with the SEBI Cyber Security Framework? Check our policies, systems, and contracts.
```

```text
I'm a new compliance officer joining next week. What regulations, policies, and past incidents should I know about?
```

---

## Step 6 — Configure Scheduled Compliance Scan

This sets up an automated weekly regulatory sweep — the "production readiness" feature.

1. Open the **Regulatory Radar** agent in the Agent Designer.
2. Click the **Schedule** tab.
3. Click **+ Add schedule**.
4. Configure:
   - **Frequency:** Weekly (Every Monday)
   - **Time:** 09:00 AM
5. In the **Prompt** field, paste:

```text
Run a weekly regulatory compliance sweep. For each regulation we track (DPDPA, GDPR, RBI Data Localization, SEBI Cyber Security, EU AI Act):
1. Check our current compliance status against each regulation
2. Flag any upcoming deadlines from the compliance calendar within the next 30 days
3. Identify any overdue remediation actions
4. Compare current status against the Board Compliance Report Q3 2025 baseline
5. Cite any past compliance incidents that remain relevant
Format as an executive compliance dashboard.
```

6. Click **Save**. The schedule becomes active after you click **Update** on the agent.

> **Demo Tip:** During a live demo, show the Schedule tab to demonstrate production readiness, then manually run the prompt to show the automated output.

---

## Step 7 — Smoke Test

Open the agent and type:

```text
Our current Data Privacy Policy allows 5-year retention for customer data and uses an opt-out consent model. A new DPDPA amendment reduces retention to 3 years and requires explicit opt-in consent. What is the impact?
```

✅ **Expected:** Impact cards with dashboards showing gaps in Data Privacy Policy (retention and consent), Data Retention SOP (manual deletion inadequate), CRM System (opt-out default), Customer Data Lake (no automated purge), with remediation actions and deadlines.

---

## Step 8 — Run the Full Demo

Open **`Demo_Script.md`** and run the 8 demo scenarios:

| Demo | Tests | Expected |
|------|-------|----------|
| 1 — DPDPA Impact | Full impact analysis | 6-8 impacts with dashboard |
| 2 — RBI Localization | Data localization gaps | Singapore DR, vendor violations |
| 3 — Compliance Check | SEBI compliance scorecard | Policy gaps with % score |
| 4 — EU AI Act | AI governance impact | Model documentation, transparency gaps |
| 5 — Cross-Regulation | Multi-regulation analysis | DPDPA + GDPR overlap |
| 6 — Scheduled Sweep | Automated compliance | Weekly executive dashboard |
| 7 — Audit Readiness | SEBI audit preparation | Readiness scorecard with evidence checklist |
| 8 — Landscape Brief | Knowledge synthesis | Comprehensive onboarding briefing |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Agent gives generic answers | Drive docs may not be indexed yet. Wait a few minutes after upload. Also try mentioning "search the Regulatory Radar Enterprise Knowledge folder in Drive" in your prompt. |
| Agent says it can't access files | Make sure the Drive connector toggle is ON. |
| Can't link sub-agents together | Use the **Combined Agent** approach (Step 4b) — one agent, all capabilities. |
| Impact analysis is too shallow | Add "search all policies, systems, and contracts" to your prompt. |
| Agent doesn't cite past incidents | Ensure `INCIDENT_Compliance_Breach_History.txt` is uploaded. Critical for institutional memory. |
| Response formatting is plain | Re-paste the latest agent instructions — they include premium formatting directives. |

---

## File Inventory

```text
Idea 2 poc/
├── Setup_Guide.md                              ← This file (START HERE)
├── Agent_Orchestrator_Instructions.txt         ← Orchestrator (multi-agent routing)
├── Agent_Regulatory_Analyzer_Instructions.txt  ← Regulatory Analyzer
├── Agent_Impact_Mapper_Instructions.txt        ← Impact Mapper
├── Agent_Combined_Instructions.txt             ← All-in-one single agent (fallback)
├── Demo_Script.md                              ← 8 demo scenarios
└── Data_Store_Docs/ (16 files)                 ← Upload ALL to Google Drive
    ├── REG_DPDPA_Amendment_2026.txt
    ├── REG_RBI_Data_Localization_Circular.txt
    ├── REG_SEBI_Cyber_Security_Framework.txt
    ├── REG_EU_AI_Act_Compliance_Notice.txt
    ├── REG_GDPR_Amendment_Cross_Border.txt
    ├── POL_Data_Privacy_Policy_v3.txt
    ├── POL_IT_Security_Policy_v2.txt
    ├── POL_Vendor_Management_Policy.txt
    ├── POL_Data_Retention_SOP.txt
    ├── POL_AI_ML_Governance_Policy.txt
    ├── SYS_Enterprise_System_Registry.txt
    ├── CONTRACT_CloudVault_Storage.txt
    ├── CONTRACT_AnalyticsPro_DataProcessor.txt
    ├── INCIDENT_Compliance_Breach_History.txt    [NEW]
    ├── RPT_Board_Compliance_Report_Q3_2025.txt  [NEW]
    └── CAL_Regulatory_Compliance_Calendar.txt   [NEW]
```
