# GenAI Guardrail Factory — Google ADK Deployment Guide

This document provides exact, detailed instructions for deploying the **GenAI Guardrail Factory** using the Google Agent Development Kit (ADK). Track 2 strictly requires terminal screenshots of ADK deployment commands and the Vertex Agent Engine UI.

This guide uses the code provided in the `Vertex_ADK_Agent` folder.

---

## Prerequisites

1. Open your **Vertex AI Workbench** instance within the Google Cloud Console.
2. Open a new Terminal window.
3. Ensure you are authenticated with Google Cloud:
   ```bash
   gcloud auth application-default login
   ```
4. Set your target project ID:
   ```bash
   gcloud config set project <YOUR_PROJECT_ID>
   ```
5. **Install ADK & Fix PATH**:
   ```bash
   pip install "google-cloud-aiplatform[agent_engines,adk]>=1.118"
   export PATH=$PATH:~/.local/bin
   ```

---

## Step 1: Install Dependencies

1. Navigate to the `Vertex_ADK_Agent` folder:
   ```bash
   cd ~/Codes/tcs-hackathon-2026/Idea\ 1\ poc/Vertex_ADK_Agent
   ```
2. Install the required Google GenAI SDK and ADK dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. *(Hackathon Tip)*: Take a screenshot of your code structure (showing `agent.py`, `tools.py`). This satisfies the **Code Architecture Checkpoint** in the rubric.

---

## Step 2: Local Execution & Testing

The rubric requires terminal screenshots showing a successful local interaction. In newer versions of the ADK, you no longer need an `init` step.

1. Navigate to the **parent** directory (the ADK CLI needs to see your folder as a package):
   ```bash
   cd ~/Codes/tcs-hackathon-2026/Idea\ 1\ poc
   ```

2. Run the local interactive loop by pointing to the agent folder:
   ```bash
   adk run Vertex_ADK_Agent
   ```

*When prompted for the entry point, enter **`agent:root_agent`** (this points to the `root_agent` object inside `agent.py`).*

---

## Step 3: Local Execution & Testing

The rubric requires terminal screenshots showing a successful local interaction.

1. Run the local interactive loop:
   ```bash
   adk run .
   ```
2. You will enter a an interactive prompt loop. Type a test prompt:
   ```text
   > Check groundedness for this response containing Vikram's PII: vikram@email.com
   ```
3. Take a screenshot showing a successful test where the agent successfully invokes its evaluation tools (like `check_pii_leakage`) and fails the prompt. This satisfies the **Local Execution Checkpoint**.

---

## Step 4: Deploy to Vertex Agent Engine

Now, you will securely deploy the local agent to Google Cloud Platform to run fully managed.

1. Run the deployment command:
   ```bash
   adk deploy agent_engine --name guardrail-evaluator --region us-central1
   ```
2. The terminal will log the packaging and deployment sequence to Vertex AI. **Wait for this process to finish successfully without errors.**
3. **Capture a high-resolution screenshot.** This image is mandatory—it satisfies the **Deployment Success Checkpoint**.

---

## Step 5: GCP Console Verification

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **Vertex AI** > **Agent Engine**.
3. Under the "Agents" tab, locate the newly deployed `guardrail-evaluator`.
4. Take a screenshot of this page showing the agent listed as `Active`/`Deployed`. This satisfies the **GCP Console Verification Checkpoint**.

---

## Step 6: Playground Validation

1. Click on the `guardrail-evaluator` agent from the Console.
2. Navigate to the **Playground** tab for that Agent.
3. In the live text box, run a query through your deployed agent:
   > "Test this output: The earth revolves around the moon."
4. Take a screenshot showing the interactive response in the Playground returning a validated Groundedness score and feedback. This satisfies the **Playground Validation Checkpoint**.

---

### You are now ready to compile your submissions!
Append the screenshots from Steps 1, 3, 4, 5, and 6 into your final PDF to fully secure the 20% score for Implementation Feasibility & Deployment.
