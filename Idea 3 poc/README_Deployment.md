# Silent Escalation Predictor — Deployment Guide

## Track 3: Customer Engagement Suite (CES)
**Tech Stack:** Dialogflow CX + Cloud Functions + App Engine  
**GCP Project:** `tcs-1771309562917`

---

## Prerequisites

- Google Cloud SDK (`gcloud`) installed and authenticated
- Project set: `gcloud config set project tcs-1771309562917`
- APIs enabled:
  ```bash
  gcloud services enable dialogflow.googleapis.com \
    cloudfunctions.googleapis.com \
    appengine.googleapis.com \
    cloudbuild.googleapis.com
  ```

---

## Step 1: Deploy the Cloud Function (Webhook)

```bash
cd "Idea 3 poc/cloud_function"

gcloud functions deploy silent-escalation-webhook \
  --gen2 \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point webhook \
  --region us-central1 \
  --source .
```

After deployment, note the **Function URL** — you'll need it for Dialogflow CX webhook configuration.

📸 **Screenshot Required:** Cloud Functions Inline Editor showing the code

---

## Step 2: Create Dialogflow CX Agent

1. Go to [Dialogflow CX Console](https://dialogflow.cloud.google.com/cx)
2. Create a new agent: **"Silent Escalation Predictor"**
3. Location: `us-central1`

### 2.1 Create Entity Types

| Entity Name | Values |
|-------------|--------|
| `@customer-id` | A-7842, B-3156, C-9281, D-4510, E-6723 |
| `@risk-tier` | Low, Medium, High |
| `@industry-segment` | SaaS, Telecom, Banking, Insurance, E-commerce, Healthcare |

### 2.2 Create Intents

| Intent Name | Training Phrases |
|-------------|-----------------|
| `analyze.customer.risk` | "Analyze risk for customer A-7842", "Check risk score for E-6723", "What's the risk level of customer C-9281", "Analyze customer B-3156" |
| `generate.intervention` | "Generate intervention for A-7842", "Create re-engagement plan for E-6723", "What intervention should we use for C-9281" |
| `view.cohort.insights` | "Show cohort insights", "What are the churn patterns for SaaS", "Cohort analysis for Telecom segment" |
| `portfolio.overview` | "Show portfolio overview", "List all at-risk customers", "Risk portfolio summary" |
| `check.risk.score` | "What's the score for A-7842", "Quick score check E-6723" |

### 2.3 Create Flows
---

### DETAILED FLOW SETUP (Single Start-Page Approach)

> **Pro Tip:** For this PoC, all logic lives on the **Start Page** of the **Default Start Flow**. No extra pages or flow transitions are needed — every user utterance matches an intent route, fires the webhook with a unique tag, and the Cloud Function returns the formatted response. This keeps the agent simple, testable, and demo-ready.

---

#### ⚠️ IMPORTANT — Do This First: Create the Webhook

You **must** create the webhook **before** adding routes, because each route references it by name.

1. In the Dialogflow CX Console, go to **Manage** (tab at the top) → **Webhooks** (left sidebar).
2. Click **+ Create**.
3. Fill in:
   | Field | Value |
   |-------|-------|
   | **Display name** | `silent-predictor-webhook` |
   | **Webhook URL** | The Cloud Function URL from Step 1 (e.g. `https://us-central1-tcs-1771309562917.cloudfunctions.net/silent-escalation-webhook`) |
   | **Method** | `POST` |
   | **Timeout** | `30` seconds (default is fine) |
4. Click **Save**.

> 💡 Find your Cloud Function URL by running:
> ```bash
> gcloud functions describe silent-escalation-webhook --region us-central1 --gen2 --format='value(serviceConfig.uri)'
> ```

---

#### 1. Configure the "Default Start Flow" — Start Page Routes

Everything happens on a single page. Navigate to: **Build** (tab) → click **Default Start Flow** in the left sidebar → click the **Start Page** node (blue circle at the top of the canvas).

In the right panel you will see a **Routes** section. Click the **+** button next to it to add each route below. You need **5 routes total**.

---

##### Route 1 — Risk Analysis (`analyze_risk`)

| Field | Value |
|-------|-------|
| **Intent** | `analyze.customer.risk` |
| **Enable webhook** | ✅ Checked |
| **Webhook** | `silent-predictor-webhook` |
| **Tag** | `analyze_risk` |
| **Transition** | End current page (or leave blank — stays on Start Page) |

Click **Save**.

**What it does:** When the user says *"Analyze risk for customer A-7842"*, Dialogflow matches the `analyze.customer.risk` intent, extracts `A-7842` as the `customer-id` parameter from the training phrases, and fires the webhook with tag `analyze_risk`. The Cloud Function returns a full risk breakdown with SRS score, 4-channel evidence, and intervention recommendation.

---

##### Route 2 — Intervention Plan (`generate_intervention`)

| Field | Value |
|-------|-------|
| **Intent** | `generate.intervention` |
| **Enable webhook** | ✅ Checked |
| **Webhook** | `silent-predictor-webhook` |
| **Tag** | `generate_intervention` |
| **Transition** | End current page |

Click **Save**.

**What it does:** Generates a personalized intervention plan with a Gemini-style re-engagement message, success probability, and approval chain based on the customer's risk tier (LOW/MEDIUM/HIGH).

---

##### Route 3 — Cohort Insights (`cohort_insights`)

| Field | Value |
|-------|-------|
| **Intent** | `view.cohort.insights` |
| **Enable webhook** | ✅ Checked |
| **Webhook** | `silent-predictor-webhook` |
| **Tag** | `cohort_insights` |
| **Transition** | End current page |

Click **Save**.

**What it does:** Returns segment-level churn intelligence (SaaS, Telecom, Banking, E-commerce, Insurance, Healthcare). If the user specifies a segment (e.g. *"cohort insights for Telecom"*), results are filtered to that segment via the `industry-segment` entity parameter.

---

##### Route 4 — Portfolio Overview (`portfolio_overview`)

| Field | Value |
|-------|-------|
| **Intent** | `portfolio.overview` |
| **Enable webhook** | ✅ Checked |
| **Webhook** | `silent-predictor-webhook` |
| **Tag** | `portfolio_overview` |
| **Transition** | End current page |

Click **Save**.

**What it does:** Returns a full portfolio summary of all 5 customers grouped by risk tier (HIGH → MEDIUM → LOW), with total at-risk ACV.

---

##### Route 5 — Quick Score Check (`check_score`)

| Field | Value |
|-------|-------|
| **Intent** | `check.risk.score` |
| **Enable webhook** | ✅ Checked |
| **Webhook** | `silent-predictor-webhook` |
| **Tag** | `check_score` |
| **Transition** | End current page |

Click **Save**.

**What it does:** Returns a one-line quick risk score for a specific customer (e.g. *"🔴 Customer E-6723 (Kavitha Nair): Silent Risk Score = 94/100 — HIGH RISK"*).

---

#### 2. How Parameter Extraction Works End-to-End

Understanding the data flow is critical for debugging:

```
User says: "Analyze risk for customer A-7842"
         ↓
Dialogflow CX: Matches intent "analyze.customer.risk"
         ↓
Entity @customer-id extracts: "A-7842"
         ↓
Parameter stored in: sessionInfo.parameters.customer-id
         ↓
Webhook fires with tag: "analyze_risk"
         ↓
Cloud Function main.py receives JSON:
  {
    "fulfillmentInfo": {"tag": "analyze_risk"},
    "sessionInfo": {"parameters": {"customer-id": "A-7842"}}
  }
         ↓
main.py extracts: params.get("customer-id") → "A-7842"
         ↓
Looks up CUSTOMERS["A-7842"] → runs calculate_srs() → returns formatted response
```

> **Note:** The Cloud Function checks for the parameter under both `customer-id` and `customer_id` keys (line 454 of `main.py`), and also normalizes to uppercase. So `a-7842`, `A-7842`, and `a-7842 ` all resolve correctly.

---

#### 3. Default Fallback (No Tag Match)

If the user sends a message that doesn't match any intent (or the webhook tag is empty/unrecognized), the Cloud Function returns a welcome message listing all available capabilities:

```
Welcome to the Silent Escalation Predictor! I can help you:

• 🔍 Analyze risk for a specific customer
• 📨 Generate intervention plans
• 📊 View cohort insights across segments
• 📋 Portfolio overview of all accounts

Try: 'Analyze risk for customer A-7842'
```

This is handled by the `else` branch at line 494 of `main.py` — no Dialogflow-side fallback intent setup is required.

---

#### SUMMARY: Final Canvas Architecture

```
Default Start Flow
└── Start Page
    ├── Route 1 (Intent: analyze.customer.risk)  → Webhook(tag: analyze_risk)
    ├── Route 2 (Intent: generate.intervention)   → Webhook(tag: generate_intervention)
    ├── Route 3 (Intent: view.cohort.insights)    → Webhook(tag: cohort_insights)
    ├── Route 4 (Intent: portfolio.overview)      → Webhook(tag: portfolio_overview)
    └── Route 5 (Intent: check.risk.score)        → Webhook(tag: check_score)
```

> **Validation:** After saving all 5 routes, click the **Start Page** node — you should see exactly 5 routes listed in the right panel. Each should show the green webhook icon (⚡) indicating a webhook is attached.


### 2.4 Configure Webhook

> ⚠️ **Already covered above** — see "Do This First: Create the Webhook" in the DETAILED FLOW SETUP section. Ensure your webhook URL is:
> ```
> https://us-central1-tcs-1771309562917.cloudfunctions.net/silent-escalation-webhook
> ```

📸 **Screenshot Required:** 
- CX Agent Flow Canvas showing all routes
- Webhooks config page showing linked URL

---

## Step 3: Deploy App Engine Frontend

1. Verify the `agent-id` and `location` in `templates/index.html`:
   ```html
   <df-messenger
       project-id="tcs-1771309562917"
       agent-id="ec92c653-4329-4aa2-a632-8b656b0ef35e"
       location="us-central1"
       language-code="en"
       max-query-length="-1">
   ```
   
   > 💡 The `location` attribute is **required** for Dialogflow CX agents. Without it, the widget defaults to `global` and returns a 404 error.

2. Enable the **Dialogflow Messenger** integration:
   - Go to Dialogflow CX Console → your agent
   - **Manage** tab → **Integrations** (left sidebar)
   - Find **"Dialogflow Messenger"** → click **Connect** / **Enable**
   - Click **Done** (the embed snippet is already in your HTML)

3. Deploy to App Engine:
   ```bash
   cd "Idea 3 poc/app_engine"
   gcloud app deploy app.yaml --project tcs-1771309562917
   ```

4. Access your app:
   ```bash
   gcloud app browse
   ```
   
   Live URL: `https://tcs-1771309562917.wl.r.appspot.com`

📸 **Screenshots Required:**
- Cloud Shell terminal showing `gcloud app deploy` success
- Hosted App Engine webpage showing embedded chat UI

---

## Step 4: Test the Full Flow

### Test Cases

1. **Risk Analysis (HIGH):**
   > "Analyze risk for customer E-6723"
   > Expected: SRS 90+, HIGH RISK, evidence from all 4 channels

2. **Risk Analysis (LOW):**
   > "Analyze risk for customer D-4510"
   > Expected: SRS <30, LOW RISK, healthy signals

3. **Intervention Generation:**
   > "Generate intervention for customer A-7842"
   > Expected: Manager escalation with personalized message

4. **Cohort Insights:**
   > "Show cohort insights for Telecom"
   > Expected: Filtered Telecom insights with weekend usage pattern

5. **Portfolio Overview:**
   > "Show portfolio overview"
   > Expected: All 5 customers with risk tiers and total at-risk ACV

6. **Quick Score Check:**
   > "What's the score for A-7842"
   > Expected: One-line SRS score with risk tier

---

## Track 3 Rubric Evidence Checklist

- [x] **Conversational Flow:** Screenshot of CX Flow Canvas with 5 intent routes
- [x] **Backend Logic:** Screenshot of Cloud Functions code editor
- [x] **Integration:** Screenshot of Webhooks config with URL linked
- [x] **Web Deployment:** Screenshot of `gcloud app deploy` terminal
- [x] **Final UI Validation:** Screenshot of App Engine webpage with chat widget
- [x] **Simulator Test:** Screenshot of CX Simulator showing webhook response

> 📁 All 16 screenshots saved in `Screenshots/` folder.

---

## File Structure

```
Idea 3 poc/
├── enterprise_docs/           # 12 knowledge documents
│   ├── Customer_Retention_Policy_2025.txt
│   ├── Intervention_Playbook_SaaS.txt
│   ├── Churn_Analysis_Q4_2025.txt
│   ├── Behavioral_Signal_Definitions.txt
│   ├── Communication_Preferences_Guidelines.txt
│   ├── Support_Escalation_SLA.txt
│   ├── Payment_Risk_Assessment_Policy.txt
│   ├── Post_Mortem_Enterprise_Churn_2024.txt
│   ├── Customer_Segmentation_Strategy.txt
│   ├── Loyalty_Program_Guidelines.txt
│   ├── GDPR_DPDPA_Customer_Data_Policy.txt
│   └── Intervention_Success_Metrics_2025.txt
├── cloud_function/            # Cloud Function webhook
│   ├── main.py
│   └── requirements.txt
├── app_engine/                # App Engine frontend
│   ├── app.yaml
│   ├── main.py
│   ├── requirements.txt
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
├── Screenshots/               # 16 deployment evidence screenshots
├── silent_predictor_architecture.png
├── Idea3_Silent_Escalation_Predictor.md
├── Idea3_Silent_Escalation_Predictor.html
└── README_Deployment.md       # This file
```

