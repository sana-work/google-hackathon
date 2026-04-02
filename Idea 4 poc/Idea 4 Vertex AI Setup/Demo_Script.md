# Decision DNA — Multi-Agent Demo Script

## 1. Business Need

In large enterprises, critical knowledge—such as Architectural Decision Records (ADRs), security policies, compliance constraints (like GDPR), and coding standards—is often scattered across wikis, Google Drive, meeting minutes, and chat histories.

When engineers design new services or write code, ensuring alignment with all historical decisions and compliance rules is a manual, error-prone, and slow process. This fragmentation leads to **architectural drift, hidden compliance violations, and bottlenecked reviews**, ultimately slowing down innovation and increasing risk.

## 2. The Solution

**Decision DNA** is a Multi-Agent Enterprise Memory System built on Google Cloud's Vertex AI and Gemini Enterprise. It transforms static enterprise documentation into an active, intelligent guardrail.

By integrating directly with Google Drive (where enterprise memory lives), Decision DNA proactively reviews draft Product Requirement Documents (PRDs), architecture proposals, and code snippets in real-time. It acts as an automated "Shift-Left" compliance and architecture review board, catching conflicts *before* they are implemented.

## 3. Idea and Architecture

The system leverages a **Multi-Agent Architecture** to handle different types of enterprise artifacts:

- **Enterprise Memory Data Store:** A centralized Google Drive containing all historical and living documents (Security Policies, GDPR Addenda, SLAs, ADRs, Meeting Minutes, Vendor Contracts, Coding Standards, Post-Mortems, Cloud Architecture Standards, Data Classification Policies). This serves as the grounding truth for the Vertex AI agents.
- **The Orchestrator:** The central routing agent that analyzes the user's input and dynamically delegates the task to the appropriate specialist sub-agent.
- **Agent 1 - Conflict Sentinel:** A specialist agent designed to parse natural language documents (e.g., PRDs, system designs). It flags policy and architectural violations and can explain *why* past decisions were made based on historical context, including citing past incidents from post-mortems.
- **Agent 2 - Code Review Judge (CRJ):** A specialist agent tailored for technical artifacts (Code, IaC, Terraform, Kubernetes YAML, SQL, configs). It reviews implementation details against enterprise coding, architecture, security, and cost governance standards.
- **Scheduled Compliance Scans:** Using Gemini Enterprise's built-in Agent Scheduler, Decision DNA can be configured to run automated compliance sweeps on a recurring basis (e.g., every Monday morning). This transforms the system from a reactive reviewer into a **proactive compliance guardian** that continuously monitors enterprise artifacts.

**Workflow:** User Input ➔ Orchestrator ➔ Specialist Agent (Sentinel or CRJ) ➔ Grounding via Google Drive ➔ Actionable Feedback with Citations.

**Scheduled Workflow:** Timer Trigger ➔ Agent auto-executes predefined compliance prompt ➔ Scans Drive documents ➔ Generates compliance report.

---

## 4. Live Demo

*Use these prompts IN ORDER during the live demo.*

═══════════════════════════════════════
DEMO 1: CONFLICT SENTINEL — PRD Review (~3 min)
═══════════════════════════════════════
PURPOSE: Show how the Orchestrator routes a document to the Conflict Sentinel and catches multiple violations.

PASTE THIS
---

Please review this draft PRD for our new "Project Aurora" microservice:

"Project Aurora is a new Customer Analytics Service that will process user behavioral data (including EU users) to generate personalized product recommendations.

Architecture:

- The service will be deployed in us-west1 (Oregon) for cost optimization.
- It will use a PostgreSQL database on Cloud SQL to store user profile embeddings.
- The service will communicate with the Order Service and Payment API via synchronous REST calls.
- To optimize storage costs, authentication and transaction audit logs will be retained for 45 days before automatic deletion.
- We plan to use raw, non-anonymized user browsing data for training our ML recommendation model.
- We are partnering with a new third-party analytics vendor (DataViz Corp) who will receive a copy of the behavioral data for dashboard generation. DataViz Corp's infrastructure is hosted in Singapore."

---

EXPECTED: 🔀 Routes to Conflict Sentinel → 5-6 conflict cards (GDPR region, log retention, sync REST vs ADR-018, Cloud SQL vs ADR-042, data minimization, vendor risk).

═══════════════════════════════════════
DEMO 2: CODE REVIEW JUDGE — Code Review (~3 min)
═══════════════════════════════════════
PURPOSE: Show the Orchestrator routing CODE to the CRJ agent for architectural and security compliance review.

PASTE THIS
---

Please review this code for our new analytics service:

```python
import requests
import psycopg2
import logging

DB_SECRET = "dummy_value_1"
ANALYTICS_TOKEN = "dummy_value_2"

def get_user_data(user_id):
    conn = psycopg2.connect(
        host="10.0.1.5",
        database="user_profiles",
        user="admin",
        password=DB_SECRET
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    user = cursor.fetchone()
    logging.info(f"Retrieved user: {user[1]} - email: {user[3]} - phone: {user[4]}")
    conn.close()
    return user

def send_to_order_service(order_data):
    response = requests.post(
        "http://order-service:8080/api/create",
        json=order_data,
        timeout=30
    )
    return response.json()

def process_analytics(user_data):
    requests.post(
        "http://dataviz-corp.external.com/ingest",
        json={"raw_user": user_data},
        headers={"Custom-Auth-Header": ANALYTICS_TOKEN}
    )
```

---

EXPECTED: 🔀 Routes to CRJ → Multiple findings:

- 🔴 REJECT: Hardcoded secrets (DB_SECRET, ANALYTICS_TOKEN) — cites Coding Standards Section 2.1
- 🔴 REJECT: SQL injection via string concatenation — cites Coding Standards Section 2.3
- 🔴 REJECT: PII logged (email, phone) — cites Coding Standards Section 3.3
- 🟡 NEEDS CHANGE: Using psycopg2/Cloud SQL instead of Firestore — cites ADR-042
- 🟡 NEEDS CHANGE: Sync REST to order-service instead of Pub/Sub — cites ADR-018
- 🟡 NEEDS CHANGE: HTTP instead of HTTPS — cites Coding Standards Section 2.4
- 🟡 NEEDS CHANGE: No error handling/retry logic — cites Coding Standards Section 4
- 🟢 ADVISORY: No health check endpoint — cites Coding Standards Section 3.4
- Overall Verdict: 🔴 BLOCKED

═══════════════════════════════════════
DEMO 3: ASK WHY — Decision Traceability (~1 min)
═══════════════════════════════════════
PURPOSE: Engineers can get instant evidence for past decisions.

TYPE THIS
---

Why did we choose Pub/Sub over gRPC? A new hire wants to use gRPC for their service
---

EXPECTED: Cites ADR-018, the cascading failure incident, rejected alternatives, and warns new sync proposals will be rejected.

═══════════════════════════════════════
DEMO 4: SAFE DRAFT — Precision Check (~30 sec)
═══════════════════════════════════════
PURPOSE: Proves the system doesn't cry wolf.

TYPE THIS
---

Review this proposal: "We will deploy a new EU-only marketing service in europe-west1. It stores pseudonymized preference flags in Firestore. Communication uses Pub/Sub (topic: marketing.preferences.updated). Audit logs retained for 180 days. No third-party vendors."
---

EXPECTED: ✅ No conflicts. Low risk. Approved.

═══════════════════════════════════════
DEMO 5: COMBINED REVIEW — Document + Code (~2 min)
═══════════════════════════════════════
PURPOSE: Show BOTH agents activated simultaneously on a mixed submission.

TYPE THIS
---

Here's our proposal and implementation for a quick notifications service:

Design: The service sends SMS notifications to users. It will query user phone numbers from Cloud SQL and use a third-party SMS vendor (TwilioClone) hosted in Brazil.

Code:

```javascript
const mysql = require('mysql');
const connection = mysql.createConnection({
  host: 'db-host',
  user: 'root',
  password: 'dummy_value_3'
});

app.post('/send-sms', (req, res) => {
  const query = "SELECT phone FROM users WHERE id = '" + req.body.userId + "'";
  connection.query(query, (err, results) => {
    console.log('Sending SMS to: ' + results[0].phone);
    fetch('http://twilioclone-brazil.com/send', {
      body: JSON.stringify({ to: results[0].phone, msg: req.body.message })
    });
    res.send('OK');
  });
});
```

---

EXPECTED: Routes to BOTH agents:

- Conflict Sentinel flags: Cloud SQL (ADR-042), vendor in Brazil (GDPR), phone numbers = PII
- CRJ flags: hardcoded password, SQL injection, PII in logs, HTTP, no error handling, no auth


═══════════════════════════════════════
DEMO 6: INSTITUTIONAL MEMORY — Post-Mortem Intelligence (~2 min)
═══════════════════════════════════════
PURPOSE: Show that the system remembers past incidents and warns when a proposal repeats a historical mistake. This demonstrates deep organizational memory beyond simple policy checking.

TYPE THIS
---

Review this proposal: "We are building a new Notifications Service. It needs to check order status from the Order Service and payment status from the Payment API before sending a notification. We will use synchronous REST calls to both services to get real-time status. The service will be deployed in us-east4."

---

EXPECTED: The agent flags the synchronous REST pattern AND cites the Post-Mortem Payment Outage (July 2024) where the exact same sync REST dependency chain caused a 23-minute outage affecting 45,000 transactions. It also cites ADR-018 (which was created as a direct result of that outage).

KEY TALKING POINT: "Notice how the agent doesn't just say 'use Pub/Sub per ADR-018.' It tells you WHAT HAPPENED the last time someone used synchronous REST between these exact services — a 23-minute outage, $180K revenue loss. This is institutional memory, not just policy checking."


═══════════════════════════════════════
DEMO 7: TERRAFORM REVIEW — Infrastructure Compliance (~2 min)
═══════════════════════════════════════
PURPOSE: Show the CRJ agent reviewing Infrastructure-as-Code for cloud architecture, cost governance, and security compliance.

PASTE THIS
---

Review this Terraform configuration for our new analytics cluster:

```
resource "google_container_cluster" "analytics" {
  name     = "analytics-cluster"
  location = "us-west1"

  node_config {
    machine_type = "n2-standard-32"
    image_type   = "UBUNTU_CONTAINERD"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]
  }

  initial_node_count = 5

  network    = "default"
  subnetwork = "default"
}

resource "google_compute_instance" "gpu_worker" {
  name         = "ml-training-gpu"
  machine_type = "a2-highgpu-1g"
  zone         = "us-west1-a"

  boot_disk {
    initialize_params {
      image = "debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}
```

---

EXPECTED: CRJ flags multiple infrastructure violations:
- us-west1 is not an approved region (Cloud Architecture Standards)
- Missing resource labels: team, environment, cost-center, project (ADR-055)
- Oversized instance (n2-standard-32) without justification (ADR-055)
- Ubuntu image instead of distroless (Security Policy / Security Checklist)
- GPU instance without FinOps approval (ADR-055)
- Using default VPC instead of shared VPC (Cloud Architecture Standards)
- Public IP on GPU instance (access_config block) (Security Policy)
- Debian OS image on compute instance (Security Policy)
- GKE Standard instead of Autopilot (Cloud Architecture Standards)
- No encryption configuration (CMEK) (Security Policy)


═══════════════════════════════════════
DEMO 8: ONBOARDING BRIEF — New Team Member (~1 min)
═══════════════════════════════════════
PURPOSE: Show the system synthesizing knowledge across ALL documents to create a contextual briefing for a new engineer joining a team.

TYPE THIS
---

I'm a new engineer joining the Payments team next week. What decisions, policies, incidents, and constraints should I know about before I start?

---

EXPECTED: A comprehensive briefing that synthesizes:
- ADR-018 (Pub/Sub mandate) with context from the Payment Outage post-mortem
- ADR-042 (Firestore) with reaffirmation from ARB Meeting #47
- Payment API SLA v2.1 (P95 < 400ms, error rate < 0.1%, change freeze windows)
- GDPR requirements for payment data
- Security Policy rules (encryption, IAM, zero trust)
- Data Classification (payment data = Tier 4 Restricted)
- The Payment Outage Post-Mortem AND the PII Leak Post-Mortem as lessons learned
- Incident Response Runbook (payments are auto-SEV-2)

KEY TALKING POINT: "With one question, the agent synthesized knowledge from 8+ documents into a personalized onboarding brief. No more two-week ramp-up reading fragmented wikis. This is enterprise knowledge made instantly accessible."


═══════════════════════════════════════
DEMO 9: SCHEDULED COMPLIANCE SCAN — Automated Proactive Guardian (~2 min)
═══════════════════════════════════════
PURPOSE: Show that Decision DNA isn't just reactive — it can be scheduled to run automated compliance sweeps, transforming it into an always-on compliance guardian.

SETUP (Do this BEFORE the demo, show the configuration during the demo):
1. In the Agent Designer, click the **Schedule** tab for your Decision DNA agent.
2. Click **+ Add schedule**.
3. Configure:
   - **Frequency:** Weekly (Every Monday)
   - **Time:** 09:00 AM
   - **Prompt:** (paste the prompt below)

SCHEDULED PROMPT:
---

Run a weekly enterprise compliance health check. Scan all documents in the Decision DNA Enterprise Memory folder and generate a Compliance Status Report covering:

1. Review all internal policies and identify any that reference outdated standards, expired certifications, or past review dates that have lapsed.

2. Check for cross-document consistency: Are any policies contradicting each other? Are ADR constraints properly reflected in coding standards and security checklists?

3. Review vendor contracts for upcoming expiry dates or certification renewal deadlines within the next 90 days.

4. Identify any compliance gaps where a regulation or policy mandate exists but no corresponding internal standard or enforcement mechanism is documented.

Format the output as a structured Compliance Status Report with sections: Critical Issues, Warnings, Upcoming Deadlines, and Recommendations.

---

EXPECTED: The agent produces a structured weekly compliance report that might flag:
- Acme Cloud contract expiring in 2026-05-31 (within 90 days threshold soon)
- Cross-validation between GDPR Addendum and Security Policy on encryption standards
- Any policies with review dates that have passed
- Gaps in coverage (e.g., no formal AI governance policy referenced)

KEY TALKING POINT: "This is the production-ready version of Decision DNA. It doesn't wait for engineers to ask — it proactively scans your entire enterprise knowledge base every Monday morning and flags compliance drift, expiring contracts, and policy gaps. Your CISO gets a report before their first coffee."

DEMO TIP: During the live demo, show the Schedule tab configuration, then manually trigger the prompt to show what the automated output would look like.
