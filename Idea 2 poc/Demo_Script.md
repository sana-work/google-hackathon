# Regulatory Change Impact Radar — Demo Script

## 1. Business Need

Regulated industries — Banking, Financial Services, Insurance, Pharma, and Healthcare — face a **relentless stream of regulatory changes**. RBI circulars, SEBI guidelines, DPDPA amendments, GDPR updates, and the EU AI Act arrive continuously. Today, compliance teams **manually read hundreds of pages** of legal text to determine which internal policies, IT systems, data flows, and vendor contracts are affected.

This process is **slow (2-6 weeks per regulation)**, **error-prone** (cross-system impacts are missed), and **reactive** (gaps are discovered during audits or after incidents — not before). A single missed regulatory requirement can cost ₹10Cr — ₹500Cr+ in penalties.

## 2. The Solution

**Regulatory Change Impact Radar** is an AI-powered Regulatory Intelligence and Impact Assessment System built on **Google Cloud's Vertex AI and Gemini Enterprise**. It acts as an **automated regulatory nervous system** that:

- **Parses** new regulatory documents and extracts every actionable requirement (clauses, deadlines, penalties)
- **Maps** those requirements against the enterprise's internal landscape — policies, IT systems, vendor contracts, and SOPs
- **Generates** prioritized impact reports showing exactly what needs to change, who owns it, and by when
- **Tracks** compliance status and remediation progress

It transforms weeks of manual expert analysis into **minutes of AI-powered intelligence**.

## 3. Architecture

The system uses a **Multi-Agent Architecture** grounded in enterprise knowledge:

- **Enterprise Knowledge Store (Google Drive):** Contains 16 enterprise documents — regulatory texts, internal policies, IT system registry, vendor contracts, SOPs, compliance breach history, board compliance reports, and a regulatory compliance calendar. This is the grounding truth for Vertex AI agents.
- **Regulatory Analyzer Agent:** Specialist agent that parses new regulatory text, extracts clauses, identifies changes from previous versions, categorizes requirements by theme, and detects cross-regulation conflicts.
- **Impact Mapper Agent:** Specialist agent that maps extracted requirements against internal assets, identifies gaps, calculates severity, cites past compliance breaches as risk amplifiers, and generates prioritized remediation plans with effort estimates.
- **Orchestrator:** Routes user requests to the correct specialist based on whether they're submitting new regulations, asking for impact analysis, checking compliance status, or requesting deadline tracking/audit readiness.
- **Scheduled Compliance Scans:** Using Gemini Enterprise's Agent Scheduler, the system runs automated weekly regulatory sweeps — scanning deadlines, compliance status, and policy gaps proactively.

**Workflow:** New Regulation ➔ Regulatory Analyzer (extract requirements) ➔ Impact Mapper (map against enterprise assets) ➔ Prioritized Impact Report with Remediation Plan.

**Scheduled Workflow:** Timer Trigger ➔ Agent auto-executes regulatory deadline and compliance sweep ➔ Generates proactive compliance report.

---

## 4. Live Demo

*Use these prompts IN ORDER during the live demo.*

═══════════════════════════════════════
DEMO 1: DPDPA AMENDMENT — Full Impact Assessment (~4 min)
═══════════════════════════════════════
PURPOSE: Show the system analyzing a new regulation and mapping its impact across policies, systems, and contracts.

TYPE THIS:
---
A new DPDPA Amendment 2026 has been notified by MeitY. Key changes:
1. Maximum data retention reduced from 5 years to 3 years
2. Consent model changed from opt-out to mandatory explicit opt-in
3. Automated deletion mechanisms are now mandatory (manual purge not acceptable)
4. Cross-border data transfer restricted to approved jurisdictions only (US is NOT approved)

Analyze the impact of this amendment on our enterprise — check our policies, IT systems, vendor contracts, and SOPs.
---

EXPECTED: 🎯 6-8 Impact cards including:
- 🔴 CRITICAL: Data Privacy Policy v3.2 — retention is 5 years, must reduce to 3 years
- 🔴 CRITICAL: Data Privacy Policy v3.2 — currently uses opt-out, must switch to opt-in
- 🔴 CRITICAL: Data Retention SOP — manual quarterly purge is not acceptable, automated deletion required
- 🟡 HIGH: CRM System — marketing consent default is "opted-in" (opt-out model), must be changed
- 🟡 HIGH: Customer Data Lake — no automated deletion, relies on manual purge
- 🟡 HIGH: AnalyticsPro Contract — sub-processor DataRefinery is in US (not approved jurisdiction)
- 🟠 MEDIUM: CloudVault Contract — Singapore DR may need review for Indian customer data
- Remediation action plan with owners, deadlines, and effort estimates


═══════════════════════════════════════
DEMO 2: RBI DATA LOCALIZATION — Vendor & System Impact (~3 min)
═══════════════════════════════════════
PURPOSE: Show the system catching data localization violations across vendors and systems.

TYPE THIS:
---
RBI has issued a new Data Localization Directive requiring ALL payment data — transactions, KYC, payment credentials — to be stored and processed exclusively within India. No foreign mirrors or DR replicas allowed outside India. What systems and contracts are affected?
---

EXPECTED: 🎯 4-5 Impact cards including:
- 🔴 CRITICAL: CRM System — DR replica in Singapore contains customer financial data
- 🔴 CRITICAL: CloudVault Contract — DR in Singapore stores organization data (may include payment-related records)
- 🔴 CRITICAL: AnalyticsPro Contract — all data in Singapore, no India DC, and sub-processor in US
- 🟡 HIGH: Vendor Management Policy — Singapore approved for DR but may conflict with RBI's "no foreign mirrors" rule
- ✅ Payment Gateway — already fully localized in India (compliant)


═══════════════════════════════════════
DEMO 3: COMPLIANCE CHECK — SEBI Cyber Security (~2 min)
═══════════════════════════════════════
PURPOSE: Show the compliance scorecard capability — checking current status against a regulation.

TYPE THIS:
---
Are we compliant with the SEBI Cyber Security and Cyber Resilience Framework? Check our IT Security Policy, vendor contracts, and system registry.
---

EXPECTED: Compliance scorecard with:
- ❌ NON-COMPLIANT: Incident reporting — our policy says 72 hours, SEBI requires 6 hours
- ❌ NON-COMPLIANT: SOC — we operate business hours only, SEBI requires 24x7 for MIIs
- ❌ NON-COMPLIANT: MFA — not enforced for application admin dashboards or DB tools
- ❌ NON-COMPLIANT: Privileged Access — standing privileges, no just-in-time provisioning, no session recording
- ⚠️ PARTIAL: Patching — our timelines are slower than SEBI mandates (7 days vs 72 hours for critical)
- ⚠️ PARTIAL: VAPT — we do annual, SEBI requires semi-annual external + quarterly internal
- ⚠️ PARTIAL: Vendor breach notification — 48 hours in contracts, SEBI requires 6 hours flow-through
- ✅ COMPLIANT: Service account inventory and access logging


═══════════════════════════════════════
DEMO 4: EU AI ACT — AI Governance Impact (~2 min)
═══════════════════════════════════════
PURPOSE: Show cross-domain impact on AI/ML governance, catching gaps across the AI policy and system registry.

TYPE THIS:
---
The EU AI Act is coming into force. We have AI models serving EU customers. What is the impact on our AI/ML Governance Policy and our deployed models?
---

EXPECTED: 🎯 5-6 Impact cards including:
- 🔴 CRITICAL: Credit Risk Scoring Model & Fraud Detection Model are HIGH RISK under EU AI Act — require conformity assessment, FRIA, and EU AI Database registration
- 🔴 CRITICAL: AI/ML Policy — customers NOT notified when AI is involved in decisions (violates transparency requirement)
- 🟡 HIGH: AI/ML Policy — Model Cards only required for HIGH IMPACT models, but EU AI Act requires documentation for all high-risk AND limited-risk systems
- 🟡 HIGH: Product Recommendation Engine — serves EU customers with AI recommendations but no AI disclosure on Customer Portal
- 🟠 MEDIUM: AI/ML Policy — quarterly drift monitoring, but EU AI Act expects continuous robustness monitoring
- 🟠 MEDIUM: Fraud Detection — "human-on-the-loop" may not meet EU AI Act's meaningful human oversight for high-risk


═══════════════════════════════════════
DEMO 5: CROSS-REGULATION — DPDPA + GDPR Overlap (~2 min)
═══════════════════════════════════════
PURPOSE: Show the system handling overlapping regulations and identifying where dual compliance is needed.

TYPE THIS:
---
We serve both Indian and EU customers. Both the new DPDPA Amendment and the GDPR Cross-Border Transfer Amendment affect us. Show me where these two regulations overlap, where they conflict, and what actions cover both.
---

EXPECTED:
- Overlapping requirements identified (consent, data transfer, retention)
- Where DPDPA is stricter (opt-in required, 3-year retention, India-approved jurisdiction list)
- Where GDPR is stricter (TIA required, new SCC Module 5, 24-hour breach notification to exporter)
- Combined remediation plan that satisfies BOTH regulations simultaneously
- Highlight: AnalyticsPro vendor contract fails BOTH regulations (Singapore without TIA, US sub-processor not approved by either)


═══════════════════════════════════════
DEMO 6: SCHEDULED REGULATORY SWEEP — Proactive Compliance Guardian (~2 min)
═══════════════════════════════════════
PURPOSE: Show that Regulatory Radar can be scheduled to run automated compliance sweeps — transforming it from reactive to proactive.

SETUP: In Agent Designer → Schedule tab, configure weekly Monday 9 AM scan.

TYPE THIS (to simulate the scheduled output):
---
Run a weekly regulatory compliance sweep. For each regulation we track (DPDPA, GDPR, RBI Data Localization, SEBI Cyber Security, EU AI Act):
1. Check our current compliance status against each regulation
2. Flag any upcoming deadlines from the compliance calendar that are within the next 30 days
3. Identify any overdue remediation actions
4. Compare current status against the Board Compliance Report Q3 2025 baseline — has anything improved or deteriorated?
5. Cite any past compliance incidents that remain relevant

Format as an executive compliance dashboard.
---

EXPECTED:
- Executive dashboard with compliance status per regulation (🟢/🟡/🔴)
- Overdue items flagged (SEBI SOC, GDPR TIA, EU AI Act conformity assessment)
- Upcoming deadlines from the calendar
- Comparison against Q3 2025 baseline showing progress or regression
- Past incidents cited as ongoing risk factors

KEY TALKING POINT: "This runs automatically every Monday. The CCO gets a compliance dashboard before the week starts — no manual effort, no missed deadlines. This is compliance on autopilot."


═══════════════════════════════════════
DEMO 7: AUDIT READINESS — Pre-Audit Preparation (~2 min)
═══════════════════════════════════════
PURPOSE: Show the agent generating a pre-audit readiness checklist, demonstrating deep institutional knowledge.

TYPE THIS:
---
SEBI is expected to conduct an on-site cyber security audit in Q2 2026. Generate an audit readiness report — for each SEBI Cyber Security Framework requirement, tell me whether we have a documented policy, whether it is implemented, and whether we can produce evidence of compliance. Also reference any past incidents relevant to our audit posture.
---

EXPECTED:
- Audit Readiness Scorecard showing ~40-50% readiness
- Per-requirement checklist with Policy/Implemented/Evidence columns
- ❌ Critical gaps: 24x7 SOC (not operational), 6-hour incident reporting (we do 72 hours), MFA on admin dashboards (not enforced)
- ⚠️ Partial: VAPT frequency, vendor breach notification timelines
- Past incident cited: COMP-2024-003 (GDPR late notification) as evidence our incident response process is slow
- Priority remediation plan targeting audit date

KEY TALKING POINT: "Instead of a compliance team spending 2 weeks preparing for an audit, the agent generates a gap analysis in seconds — with specific evidence requirements and remediation priorities. It even cites our past breaches as risk indicators."


═══════════════════════════════════════
DEMO 8: REGULATORY LANDSCAPE BRIEF — Compliance Officer Onboarding (~2 min)
═══════════════════════════════════════
PURPOSE: Show the agent synthesizing knowledge from 16+ documents into a comprehensive onboarding brief.

TYPE THIS:
---
I'm a new compliance officer joining the organization next week. I'll be responsible for BFSI regulatory compliance across India and EU. Give me a comprehensive brief: what regulations affect us, what systems and vendors handle regulated data, what are our current compliance gaps, what deadlines are coming up, and what past compliance incidents should I know about?
---

EXPECTED: A comprehensive landscape brief including:
- All 5 regulations summarized with jurisdiction and key requirements
- Current compliance status per regulation (from Board Report baseline)
- Key systems: CRM (Singapore DR issue), Customer Data Lake (no automated deletion), Payment Gateway (compliant), HR System (EU data for Indian employees)
- Key vendors: CloudVault (India + Singapore), AnalyticsPro (Singapore + US sub-processor — highest risk)
- Top compliance gaps: SEBI SOC, DPDPA consent model, EU AI Act conformity
- Upcoming deadlines from the calendar
- All 3 past compliance incidents with lessons learned
- Recommended reading list prioritized by urgency

KEY TALKING POINT: "A new compliance officer normally spends 2-4 weeks reading fragmented documents across wikis and shared drives. Regulatory Radar synthesizes 16 enterprise documents into a personalized, actionable briefing in seconds. This is institutional knowledge made instantly accessible."
