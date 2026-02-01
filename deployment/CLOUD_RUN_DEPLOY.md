# ☁️ Cloud Run Deployment Guide: Aegis-OS

This guide provides the exact steps to deploy **Aegis-OS** to Google Cloud Run, fulfilling one of the key technical requirements for the **Google AI Challenge**.

---

## 🛠️ Prerequisites

1.  **Google Cloud Project**: Create one at [console.cloud.google.com](https://console.cloud.google.com).
2.  **Billing Enabled**: Cloud Run requires an active billing account (Free Tier available).
3.  **GCP SDK**: Install the `gcloud` CLI on your machine.
4.  **APIs Enabled**:
    ```bash
    gcloud services enable run.googleapis.com \
                           cloudbuild.googleapis.com \
                           secretmanager.googleapis.com
    ```

---

## 🏗️ Step 1: Build with Cloud Build

We will use Google’s remote builder to create your container image and store it in the Artifact Registry.

```bash
# 1. Set your project ID
gcloud config set project [YOUR_PROJECT_ID]

# 2. Build the image (relying on the included Dockerfile)
gcloud builds submit --tag gcr.io/[YOUR_PROJECT_ID]/aegis-os
```

---

## 🛡️ Step 2: Secret Management (Best Practice)

Judgment for the AI Challenge favors **secure production patterns**. Instead of passing API keys as plain text, use **Secret Manager**.

1.  **Create the secrets**:
    ```bash
    echo -n "your-gemini-key" | gcloud secrets create GEMINI_API_KEY --data-file=-
    echo -n "your-rag-key" | gcloud secrets create RAG_API_KEY --data-file=-
    ```

2.  **Grant access** to the Cloud Run service account:
    ```bash
    gcloud secrets add-iam-policy-binding GEMINI_API_KEY \
      --member="serviceAccount:[PROJECT_NUMBER]-compute@developer.gserviceaccount.com" \
      --role="roles/secretmanager.secretAccessor"
    ```

---

## 🚀 Step 3: Deploy to Cloud Run

Deploy the container and map the secrets to your environment variables.

```bash
gcloud run deploy aegis-os \
  --image gcr.io/[YOUR_PROJECT_ID]/aegis-os \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets="NEXT_PUBLIC_GEMINI_API_KEY=GEMINI_API_KEY:latest,NEXT_PUBLIC_RAG_API_KEY=RAG_API_KEY:latest"
```

---

## 💡 Why this configuration?

-   **`output: 'standalone'`**: Next.js 15 optimization that reduces container size by ~80% by only including necessary files.
-   **Port 8080**: Cloud Run’s standard entry port (configured in your Dockerfile).
-   **Alpine Base**: Minimizes the attack surface and boot time of your industrial HUD.
-   **Secret Injection**: Keeps your competition keys safe while deployed.

---

## 🔄 Updating the Deployment

Whenever you push new code to GitHub:
1.  Run the `gcloud builds submit` command again.
2.  Run `gcloud run deploy` (or set up a GitHub Action to automate this).

**Source**: Google AI Challenge Deployment Requirements
**Related Workflow**: [.agent/workflows/deploying-to-aks.md](file:///d:/my-dev-knowledge-base/.agent/workflows/deploying-to-aks.md) (Alternative)
