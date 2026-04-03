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

#### Default Start Flow
- **Start Page** → Route intents to respective pages
- Add **conversation starters** (suggested chips):
  - "🔍 Analyze customer A-7842"
  - "📨 Generate intervention for E-6723"
  - "📊 Show cohort insights"
  - "📋 Portfolio overview"

#### Risk Analysis Flow
1. **Collect Customer ID** (Page with form parameter: `customer-id`)
2. **Call Webhook** with tag: `analyze_risk`
3. **Display Results** → Return to start

#### Intervention Flow
1. **Collect Customer ID** (reuse or new)
2. **Call Webhook** with tag: `generate_intervention`
3. **Display Intervention Plan** → Return to start

#### Cohort Insights Flow
1. **Optional: Collect Segment** (`industry-segment`)
2. **Call Webhook** with tag: `cohort_insights`
3. **Display Insights** → Return to start

#### Portfolio Flow
1. **Call Webhook** with tag: `portfolio_overview`
2. **Display Portfolio** → Return to start

### 2.4 Configure Webhook

1. Go to **Manage → Webhooks**
2. Create webhook: **"silent-predictor-webhook"**
3. URL: `YOUR_CLOUD_FUNCTION_URL` (from Step 1)
4. Method: POST

📸 **Screenshot Required:** 
- CX Agent Flow Canvas showing all flows
- Webhooks config page showing linked URL

---

## Step 3: Deploy App Engine Frontend

1. Update the `agent-id` in `templates/index.html`:
   ```html
   <df-messenger
       project-id="tcs-1771309562917"
       agent-id="YOUR_ACTUAL_AGENT_ID"
       ...>
   ```
   
   Find your Agent ID in Dialogflow CX Console → Agent Settings

2. Deploy to App Engine:
   ```bash
   cd "Idea 3 poc/app_engine"
   gcloud app deploy app.yaml --project tcs-1771309562917
   ```

3. Access your app:
   ```bash
   gcloud app browse
   ```

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

---

## Track 3 Rubric Evidence Checklist

- [ ] **Conversational Flow:** Screenshot of CX Flow Canvas
- [ ] **Backend Logic:** Screenshot of Cloud Functions code editor
- [ ] **Integration:** Screenshot of Webhooks config with URL linked
- [ ] **Web Deployment:** Screenshot of `gcloud app deploy` terminal
- [ ] **Final UI Validation:** Screenshot of App Engine webpage with chat

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
├── silent_predictor_architecture.png
├── Idea3_Silent_Escalation_Predictor.md
├── Idea3_Silent_Escalation_Predictor.html
└── README_Deployment.md       # This file
```
