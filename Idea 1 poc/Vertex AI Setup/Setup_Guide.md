# GenAI Guardrail Factory — Setup Guide

> **Environment:** GCP Project `tcs-1770741136478`
> **Platform:** VM with Anaconda Python, Sentence Transformers
> **Primary Interface:** FastAPI Server + Interactive Dashboard

---

## Prerequisites

1. **GCP Project** with Vertex AI API enabled
2. **Gemini API** enabled in the project
3. **Anaconda Python** (pre-installed on VM)
4. Internet access for `pip install` (one-time)

## 🔑 Critical: Authentication Setup
This app now supports both authentication paths below:

### Option A — Vertex AI (recommended for GCP projects)
Before running the server, ensure your environment has access to Google Cloud Vertex AI. Run the following command in your terminal:

```bash
gcloud auth application-default login
```
*Follow the browser prompts to log in. This creates the "Application Default Credentials" (ADC) needed by the Python SDK.*

### Option B — Gemini Developer API (good fallback if Vertex AI is blocked)
Set an API key before starting the server:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

The backend also accepts `GOOGLE_API_KEY`. The dashboard can send a session-only fallback key to the server, but it is **not** written to project files.

### Optional — Control Plane Protection

To protect `/api/*` routes with an admin token:

```bash
export GUARDRAIL_ADMIN_TOKEN="replace-with-a-long-random-secret"
```

Paste that same value into the dashboard's **Admin Token** field before running stages.

---

## 🚀 Quick Start

### Step 1 — Upload Files

Upload the entire `Vertex AI Setup/` folder to the VM:

```text
Vertex AI Setup/
├── server.py                 ← FastAPI backend (start here)
├── pipeline.py               ← Core pipeline engine
├── Dashboard.html            ← Interactive dashboard (served by FastAPI)
├── requirements.txt          ← Python dependencies
├── Setup_Guide.md            ← This file
├── Demo_Script.md            ← Demo narration
├── 01_Setup_and_RAG_App.ipynb
├── 02_Adversarial_Test_Generator.ipynb
├── 03_Evaluation_Pipeline.ipynb
├── 04_Auto_Remediation.ipynb
└── Data_Store_Docs/          ← 6 enterprise knowledge docs
    ├── HR_Leave_Policy.txt
    ├── IT_Security_Policy.txt
    ├── Employee_Handbook.txt
    ├── Data_Privacy_Policy.txt
    ├── Compensation_Benefits_Guide.txt
    └── Incident_Response_SOP.txt
```

### Step 2 — Install Dependencies

```bash
cd "Vertex AI Setup"
pip install -r requirements.txt
```

### Step 3 — Enable GCP APIs

In the GCP Console (`console.cloud.google.com`):

1. Navigate to **APIs & Services** → **Enable APIs**
2. Enable:
   - **Vertex AI API** (`aiplatform.googleapis.com`)
   - **Generative Language API** (for Gemini)
   - **BigQuery API** (`bigquery.googleapis.com`) if you want cloud run-history archiving

### Step 4 — Run the Server

```bash
python server.py
```

Open **http://localhost:8000** in Chrome. The dashboard is interactive — click through 4 stages:

| Stage | What Happens | Button |
| --- | --- | --- |
| **1. Setup** | Loads docs, builds RAG app with ChromaDB | "Initialize Pipeline" |
| **2. Test Gen** | Gemini generates 50 adversarial attacks | "Generate Adversarial Tests" |
| **3. Evaluate** | Scores all responses, shows dashboard | "Run Full Evaluation" |
| **4. Remediate** | Gemini diagnoses & fixes failures | "Run Auto-Remediation" |

### Optional — Enable BigQuery Run Archive

If you want every evaluation/remediation run archived to BigQuery:

1. Enable the **BigQuery API**
2. In the dashboard, open **Cloud Archive & Fallbacks**
3. Set **Archive Run History** to `BigQuery`
4. Leave the defaults or set:
   - Dataset: `guardrail_factory`
   - Table Prefix: `guardrail`
   - Location: `US`

The app will create and write to:

- `<dataset>.<table_prefix>_runs`
- `<dataset>.<table_prefix>_failed_cases`

If `google-cloud-bigquery` is missing, the UI will show a dependency warning instead of silently failing.

### Optional — Demo Mode For Hackathon Presentation

Use **Demo Mode (Deterministic)** in the left control rail when you need a stable, repeatable walkthrough that does not depend on live model behavior.

---

## Alternative: Jupyter Notebooks

If you prefer running step-by-step in Vertex AI Workbench:

1. Open Vertex AI Workbench in GCP Console
2. Upload the notebooks and `Data_Store_Docs/` folder
3. Run in order: `01` → `02` → `03` → `04`
4. Open `Dashboard.html` in Chrome to see the visual dashboard

---

## Troubleshooting

| Issue | Fix |
| --- | --- |
| `ModuleNotFoundError: google.genai` | `pip install google-genai` or `pip install -r requirements.txt` |
| `ModuleNotFoundError: chromadb` | `pip install chromadb` |
| `ModuleNotFoundError: fastapi` | `pip install fastapi uvicorn` |
| Permission denied API errors | Enable Vertex AI API; ensure service account has `Vertex AI User` role |
| `No working model found via Vertex AI or Developer API` | Set `GEMINI_API_KEY` or `GOOGLE_API_KEY`, or paste the key into the dashboard session field |
| BigQuery archive says `dependency_missing` | Run `pip install -r requirements.txt` so `google-cloud-bigquery` is available |
| BigQuery archive says `error` | Enable the BigQuery API and ensure the current identity can create datasets/tables and insert rows |
| Dashboard says `Unauthorized` | Set `GUARDRAIL_ADMIN_TOKEN` on the server and paste the same value into the dashboard `Admin Token` field |
| Quota exceeded | Add `time.sleep(2)` between calls or reduce tests-per-category to 5 |
| Port 8000 already in use | `python server.py` uses port 8000; kill existing or use `lsof -i :8000` |
