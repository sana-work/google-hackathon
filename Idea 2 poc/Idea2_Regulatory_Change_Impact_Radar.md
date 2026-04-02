# Regulatory Change Impact Radar

## AI-Powered Regulatory Intelligence & Impact Assessment System

**Google AI Track:** Intelligent Search & Gemini Enterprise  
**Submission Date:** February 2026  
**tcs^AI Google Hackathon 2026 — Ideathon Phase**

---

## 1. Executive Summary

The **Regulatory Change Impact Radar** is an AI-powered system that automatically monitors regulatory changes, maps them against an enterprise's internal policies, systems, and processes, and generates prioritized impact assessments with remediation action plans. It transforms reactive, manual compliance analysis into a proactive, automated regulatory intelligence engine.

---

## 2. Problem Statement

### The Challenge

Regulated industries — BFSI, pharma, healthcare, telecom — face a **relentless stream of regulatory changes**. RBI circulars, SEBI guidelines, FDA guidance documents, GDPR amendments, DPDPA notifications, and industry-specific mandates arrive continuously. Today, compliance teams **manually read hundreds of pages** to determine which internal policies, SOPs, IT systems, data flows, and contracts are affected.

### Scale of the Problem

| Metric | Typical Enterprise Reality |
|--------|---------------------------|
| **Regulatory updates per year** | 300-500+ across jurisdictions |
| **Pages per regulation** | 20-200+ pages of legal text |
| **Internal policies affected** | 50-500 per organization |
| **Time to assess one change** | 2-6 weeks of expert analysis |
| **Cost of non-compliance** | ₹10Cr - ₹500Cr+ in penalties |
| **Teams involved** | Legal, Compliance, IT, Operations, Risk |

### Why Current Approaches Fail

1. **Manual reading doesn't scale** — compliance teams can't keep pace with regulatory volume
2. **Cross-impact analysis is nearly impossible manually** — a single regulation may affect 10+ policies, 5 IT systems, and 3 vendor contracts
3. **Tribal knowledge dependency** — only a few experts understand the full landscape of internal policies
4. **Reactive discovery** — impacts are often found after deadlines, during audits, or after incidents
5. **No institutional memory** — previous impact assessments aren't systematically captured or reused

### Who Faces This Problem?

- **Banking & Financial Services**: RBI, SEBI, IRDAI regulations
- **Healthcare & Pharma**: FDA, CDSCO, clinical trial regulations
- **Telecom**: TRAI, DoT policy changes
- **Cross-industry**: Data protection (GDPR, DPDPA), ESG reporting (BRSR, CSRD)
- **TCS consulting teams** managing compliance for enterprise clients

---

## 3. Proposed Solution

### Core Concept

An AI system that creates an **automated regulatory nervous system** — continuously scanning for changes and instantly mapping their impact across the enterprise's internal landscape, powered by Gemini's long-context understanding and Vertex AI Search.

### Key Capabilities

#### 3.1 Regulatory Monitoring Engine

- Continuously monitors designated regulatory sources (government gazettes, regulator websites, industry body publications)
- Detects new or amended regulations relevant to the enterprise's industry and geography
- Uses **Gemini 1.5 Pro** to parse complex legal language and extract:
  - Regulatory clauses and requirements
  - Effective dates and compliance deadlines
  - Scope of applicability
  - Penalties for non-compliance

#### 3.2 Enterprise Asset Knowledge Graph

Maintains a semantic knowledge graph of the enterprise's internal landscape:

```
                    ┌─────────────┐
                    │  Policies   │
                    └──────┬──────┘
                           │
    ┌─────────┐     ┌──────┴──────┐     ┌──────────────┐
    │  SOPs   │────▶│  Knowledge  │◀────│  IT Systems  │
    └─────────┘     │    Graph    │     └──────────────┘
                    └──────┬──────┘
                           │
    ┌─────────┐     ┌──────┴──────┐     ┌──────────────┐
    │  Data   │────▶│ Relationships│◀────│   Vendor     │
    │  Flows  │     │ & Dependencies│    │  Contracts   │
    └─────────┘     └─────────────┘     └──────────────┘
```

- Each asset is semantically indexed with its purpose, scope, related regulatory domains, and dependencies
- Relationships between assets are explicitly mapped (e.g., "Policy P1 governs System S3 which processes Data Flow D7")

#### 3.3 Automated Impact Analysis

When a new regulation is detected, the system:

1. **Semantically matches** regulatory clauses against the knowledge graph
2. **Identifies affected assets** with specific clause-to-policy mappings
3. **Generates a structured impact report:**

| Field | Example |
|-------|---------|
| **Regulation** | DPDPA Amendment 2026 — Section 4(2)(b) |
| **Affected Policy** | Data Privacy Policy v3.2 — Clause 8.1 (Data Retention) |
| **Impact Type** | Policy update required — retention period must be reduced from 5 years to 3 years |
| **Severity** | HIGH |
| **Affected Systems** | CRM Database, Customer Data Lake, Backup Systems |
| **Affected Contracts** | Vendor Agreement #V-2024-087 (Cloud Storage Provider) — SLA clause on data deletion |
| **Compliance Deadline** | 90 days from notification (June 15, 2026) |
| **Estimated Effort** | 35 person-days |

#### 3.4 Remediation Action Tracker

- Auto-generates remediation tasks with suggested owners, deadlines, and dependency chains
- Prioritizes actions by severity × deadline proximity
- Tracks completion status with evidence of compliance

#### 3.5 Audit & Evidence Trail

- Every impact assessment is versioned and traceable
- Auditors can follow: Regulation → Impact Analysis → Remediation → Evidence of Completion
- Supports regulatory examination readiness

---

## 4. Architecture

### System Architecture Diagram

![Regulatory Change Impact Radar - Architecture Diagram](/Users/sanaiqbal/.gemini/antigravity/scratch/tcs-hackathon-2026/regulatory_radar_architecture.png)

### Google AI Technology Stack

| Component | Google Service | Purpose |
|-----------|---------------|---------|
| Document Understanding | **Gemini 1.5 Pro** | Long-context parsing of 100+ page regulatory documents |
| Semantic Search | **Vertex AI Search** | RAG-based retrieval over knowledge graph |
| Document Extraction | **Document AI** | Structured extraction from regulatory PDFs/policies |
| Monitoring | **Cloud Functions + Cloud Scheduler** | Scheduled scanning of regulatory sources |
| Data Storage | **BigQuery** | Regulatory change history & impact assessments |
| Knowledge Graph | **Vertex AI Vector Search** | Semantic linking of policies, systems, and regulations |
| Visualization | **Looker** | Impact dashboard & compliance status |
| Access Control | **Cloud IAM** | Role-based access to compliance data |

---

## 5. Implementation Approach

### Phase 1: PoC (2-3 weeks)

- Ingest 5-10 synthetic regulatory documents + 10-15 synthetic internal policies
- Build knowledge graph with basic relationships
- Implement impact analysis for new regulation upload
- Generate structured impact report with severity ratings

### Phase 2: MVP (4-6 weeks)

- Add automated regulatory source monitoring
- Expand knowledge graph to include IT systems, data flows, and contracts
- Implement remediation action tracker
- Build compliance status dashboard

### Phase 3: Production (8-12 weeks)

- Multi-jurisdiction support (Indian regulators, EU, US)
- Integration with GRC platforms (ServiceNow, Archer)
- Historical trend analysis and prediction
- API for client-specific customization

---

## 6. Novelty & Differentiation

| Aspect | Existing Solutions | Regulatory Change Impact Radar |
|--------|--------------------|-----------------------------|
| **Monitoring** | Manual reading of regulatory websites | Automated, continuous scanning |
| **Analysis** | Expert reads regulation + guesses impact | Semantic matching against knowledge graph |
| **Scope** | One regulation at a time | Cross-regulation, cross-asset impact analysis |
| **Speed** | Weeks to months | Hours to days |
| **Output** | Word document summary | Structured report + action tracker + audit trail |
| **Intelligence** | Reactive — after the fact | Proactive — radar detects changes as they happen |

### Why This Idea Is Unique

1. **Not "search over documents"** — it's **structured impact intelligence** with cross-system mapping
2. **Knowledge graph approach** — maps relationships between policies, systems, and regulations that flat search can't capture
3. **Actionable output** — doesn't just flag changes, generates remediation plans with effort estimates
4. **Massive TCS relevance** — directly applicable to BFSI consulting, the largest TCS vertical

---

## 7. Business Value

### Quantitative Impact

- **80-90% reduction** in regulatory impact assessment time (weeks → hours)
- **95%+ coverage** of cross-system dependencies (vs. 60-70% with manual analysis)
- **Prevents compliance gaps** — catches impacts that manual analysis misses
- **Saves ₹2-5 Cr annually** per large enterprise client in compliance team labor costs

### Strategic Value for TCS

- **Consulting differentiator**: Offer "Regulatory Intelligence-as-a-Service" to BFSI clients
- **Risk mitigation**: Protect clients from penalty exposure (often hundreds of crores)
- **Account growth**: Deep compliance integration strengthens client relationships
- **Platform play**: Can be white-labeled and offered across client accounts

### Long-term Sustenance

- Regulatory complexity is **increasing globally** (EU AI Act, DPDPA, CSRD, etc.)
- The knowledge graph becomes **more valuable over time** as more policies and regulations are mapped
- Applicable across all regulated industries, not limited to one domain

---

## 8. Security & Compliance

| Aspect | Implementation |
|--------|---------------|
| **Access Control** | Role-based access — compliance team, legal, IT, auditors |
| **Data Privacy** | No real client data in PoC; synthetic policies and regulations |
| **Audit Trail** | Every impact assessment versioned and traceable |
| **Human-in-the-loop** | AI recommends impacts; compliance officers validate and approve |
| **Data Residency** | Deployment on Google Cloud regions compliant with local regulations |
| **Responsible AI** | Explainable — every impact finding cites specific regulatory clauses + policy sections |
| **Confidentiality** | Enterprise policies stored with encryption at rest and in transit |

---

## 9. PoC Demonstration Plan

### Synthetic Dataset

- **5 regulatory documents** (modeled on DPDPA, RBI data localization, SEBI cyber security guidelines)
- **15 internal policies/SOPs** covering data privacy, IT security, vendor management, data retention, incident response
- **5 IT systems** (CRM, Data Lake, Payment Gateway, HR System, Customer Portal)
- **3 vendor contracts** with relevant SLA and compliance clauses

### Demo Flow

```
Step 1: Show the enterprise knowledge graph — policies, systems, contracts linked
Step 2: Upload a new "regulatory circular" (synthetic)
Step 3: System processes and extracts regulatory requirements
Step 4: Impact report generated — 3 policies affected, 2 systems impacted, 1 contract needs review
Step 5: Severity ratings assigned (1 Critical, 1 High, 1 Medium)
Step 6: Remediation actions auto-generated with owners and deadlines
Step 7: Show audit trail linking regulation → impact → remediation
```

---

## 10. Use Case Examples

### Example 1: Data Localization Regulation
>
> **Regulation**: New circular mandating all financial data must be stored within India within 180 days.  
> **Impact detected**: Cloud storage vendor contract allows data residency in Singapore. Customer Data Lake replication to EU region violates requirement. 3 policies need localization clause updates.  
> **Actions generated**: Vendor renegotiation task (Legal team, 60 days), Data Lake migration task (IT team, 120 days), Policy updates (Compliance team, 30 days).

### Example 2: Consent Management Update
>
> **Regulation**: Amended data protection rule requiring explicit opt-in consent for marketing communications.  
> **Impact detected**: Current privacy policy assumes opt-out model. CRM system's default consent flag is "opted-in." Marketing email SOP doesn't include consent verification step.  
> **Actions generated**: Policy rewrite (Legal, 15 days), CRM system change request (IT, 45 days), SOP update (Marketing operations, 20 days).

---

*This document is submitted as part of the tcs^AI Google Hackathon 2026 — Ideathon Phase. All data used is synthetic. No real client names, PII, or confidential information is included.*
