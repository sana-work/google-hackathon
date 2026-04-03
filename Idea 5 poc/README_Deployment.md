# Policy-to-Flow Compiler — Deployment Guide
## Track 3: Customer Engagement Suite | TCS^AI Hackathon 2026

---

### Prerequisites
- GCP Project: `tcs-1771309562917`
- Region: `us-central1`
- gcloud CLI authenticated

---

## Step 1: Deploy Cloud Function

```bash
cd cloud_function

gcloud functions deploy policy-flow-webhook \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=webhook \
  --trigger-http \
  --allow-unauthenticated \
  --memory=256MB \
  --timeout=60s
```

**Webhook URL:** `https://us-central1-tcs-1771309562917.cloudfunctions.net/policy-flow-webhook`

---

## Step 2: Create Dialogflow CX Agent

1. Go to: https://dialogflow.cloud.google.com/cx
2. Select project `tcs-1771309562917`, region `us-central1`
3. Create agent: **Policy-to-Flow Compiler**

### 2a. Create Webhook
| Field | Value |
|-------|-------|
| Name | `policy-flow-webhook` |
| URL | `https://us-central1-tcs-1771309562917.cloudfunctions.net/policy-flow-webhook` |

### 2b. Create 5 Intents + Routes

| Intent | Training Phrases | Webhook Tag |
|--------|-----------------|-------------|
| `compile.policy` | "Compile return policy", "Parse the KYC policy", "Compile warranty policy" | `compile_policy` |
| `fuzz.test` | "Run fuzz test on return policy", "Fuzz the KYC policy", "Test warranty compliance" | `fuzz_test` |
| `check.compliance` | "Check compliance for return scenario", "Is this case compliant?", "Verify scenario" | `check_compliance` |
| `explain.node` | "Explain node CHECK_PACKAGING", "What does FREEZE_ACCOUNT do?", "Show node logic" | `explain_node` |
| `runtime.query` | "I want to return a laptop", "What's the KYC process?", "My phone has a defect" | `runtime_query` |

### 2c. Add Routes on Start Page
For each intent → Enable webhook → Select `policy-flow-webhook` → Set tag

### 2d. Copy Agent ID
Settings → General → Copy the Agent ID for the frontend.

---

## Step 3: Update Frontend Agent ID

Edit `app_engine/templates/index.html`, replace:
```
agent-id="AGENT_ID_PLACEHOLDER"
```
with your actual agent ID.

---

## Step 4: Deploy App Engine

```bash
cd app_engine

gcloud app deploy app.yaml --project=tcs-1771309562917 --quiet
```

**Frontend URL:** `https://tcs-1771309562917.wl.r.appspot.com`

> ⚠️ If Idea 3 is already deployed to the default service, deploy Idea 5 as a named service:
> ```bash
> # Add to app.yaml: service: policy-flow
> gcloud app deploy app.yaml --project=tcs-1771309562917 --quiet
> ```
> URL: `https://policy-flow-dot-tcs-1771309562917.wl.r.appspot.com`

---

## Step 5: Test All Flows

| # | Test | Input | Expected |
|---|------|-------|----------|
| 1 | Compile | "Compile return policy" | 12 nodes, 6 entities, DSL output |
| 2 | Compile | "Compile KYC policy" | 12 nodes, 5 entities, tier logic |
| 3 | Fuzz | "Run fuzz test on return policy" | 2847 paths, 98.4%, 1 critical gap |
| 4 | Fuzz | "Fuzz warranty policy" | 3412 paths, 99.1%, 0 gaps |
| 5 | Compliance | "Check compliance for laptop return" | Pass/Fail with rule citation |
| 6 | Node | "Explain CHECK_PACKAGING node" | Node logic + policy reference |
| 7 | Runtime | "I want to return a laptop" | Disclaimer stated, entity extraction |

---

## Track 3 Screenshot Checklist

- [ ] Conversational Flow: CX Flow Canvas with 5 intent routes
- [ ] Backend Logic: Cloud Functions Inline Editor (main.py)
- [ ] Integration: Webhook config with Cloud Function URL
- [ ] Web Deployment: `gcloud app deploy` terminal success
- [ ] Final UI: App Engine webpage with embedded df-messenger chat

---

## File Structure

```
Idea 5 poc/
├── Idea5_Policy_to_Flow.md          # Ideathon document
├── policy_to_flow_architecture.png  # Architecture diagram
├── index.html                       # Original standalone demo UI
├── README_Deployment.md             # This file
├── cloud_function/
│   ├── main.py                      # Webhook (5 tags)
│   └── requirements.txt
├── app_engine/
│   ├── app.yaml
│   ├── main.py                      # Flask server
│   ├── requirements.txt
│   └── templates/
│       └── index.html               # Enhanced UI + df-messenger
└── Screenshots/                     # Evidence screenshots
```
