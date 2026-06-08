# 🏦 BankCore MLOps — Azure End-to-End Banking Intelligence Platform


![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Azure ML](https://img.shields.io/badge/Azure-Machine%20Learning-0078D4)
![AKS](https://img.shields.io/badge/Azure-AKS-0078D4)
![Azure DevOps](https://img.shields.io/badge/Azure-DevOps-0078D4)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688)
![MLflow](https://img.shields.io/badge/MLflow-2.x-0194E2)
![License](https://img.shields.io/badge/License-MIT-green)

---
[![View Interactive README](https://img.shields.io/badge/View-Interactive%20README-0078D4?style=for-the-badge&logo=microsoftazure)](https://2209aditya.github.io/BankCore-MLOps-Azure-End-to-End-Banking-Intelligence-Platform)
## 📌 Overview

A production-grade MLOps platform purpose-built for banking — covering customer intelligence, real-time fraud detection, credit risk scoring, churn prediction, and regulatory compliance. Built entirely on Azure-native services with enterprise security, full auditability, and AI-powered decisioning at its core.

Built for reproducibility, scalability, and zero-trust security using Azure Managed Identity throughout.

---

## 🏗️ Azure Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           AZURE SUBSCRIPTION                                 │
│                                                                              │
│  ┌─────────────────────────┐    ┌────────────────────────────────────────┐  │
│  │  Data Layer              │    │  ML Platform                           │  │
│  │  ──────────────────────  │    │  ─────────────────────────────────── │  │
│  │  ADLS Gen2               │───▶│  Azure Machine Learning Workspace      │  │
│  │  (raw / processed /      │    │  • Compute Clusters (CPU/GPU)          │  │
│  │   curated zones)         │    │  • AML Feature Store                   │  │
│  │                          │    │  • MLflow Experiment Tracking          │  │
│  │  Azure Data Factory      │    │  • Model Registry (versioned)          │  │
│  │  (ingestion / ETL)       │    │                                        │  │
│  └─────────────────────────┘    └──────────────┬─────────────────────────┘  │
│                                                 │                            │
│  ┌─────────────────────────┐    ┌──────────────▼─────────────────────────┐  │
│  │  CI/CD                   │    │  Serving Layer                         │  │
│  │  ──────────────────────  │    │  ─────────────────────────────────── │  │
│  │  Azure DevOps Pipelines  │───▶│  Azure Kubernetes Service (AKS)       │  │
│  │  • CI: lint, test, build │    │  • Real-time inference pods            │  │
│  │  • CD: train, eval, ship │    │  • Horizontal Pod Autoscaler           │  │
│  │  • Azure Repos (Git)     │    │                                        │  │
│  │                          │    │  AML Managed Online Endpoints          │  │
│  │  Azure Container         │    │  Azure Container Registry (ACR)        │  │
│  │  Registry (ACR)          │    └──────────────┬─────────────────────────┘  │
│  └─────────────────────────┘                   │                            │
│                                                 │                            │
│  ┌──────────────────────────────────────────────▼─────────────────────────┐  │
│  │  Monitoring & Security                                                  │  │
│  │  Azure Monitor • Application Insights • Azure Key Vault                │  │
│  │  Log Analytics Workspace • Microsoft Defender for Cloud                │  │
│  │  Azure OpenAI Service (AI Banker Assistant)                            │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
bankcore-mlops/
├── .azure/
│   └── pipelines/
│       ├── ci-pipeline.yml                  # Lint, test, Docker build, ACR push
│       ├── cd-pipeline.yml                  # Train, evaluate, deploy to AKS
│       └── training-pipeline.yml            # AML training pipeline trigger
│
├── infra/
│   ├── main.bicep                           # Root Bicep deployment
│   └── modules/
│       ├── aml_workspace.bicep
│       ├── storage_adls.bicep               # ADLS Gen2 + zones
│       ├── aks_cluster.bicep
│       ├── acr.bicep
│       ├── keyvault.bicep
│       ├── openai.bicep                     # Azure OpenAI Service
│       └── monitor.bicep
│
├── src/
│   ├── data/
│   │   ├── adls_connector.py                # ADLS Gen2 read/write
│   │   ├── adf_trigger.py                   # ADF pipeline trigger
│   │   ├── feature_store.py                 # AML Feature Store client
│   │   └── validation.py                    # Schema & quality checks
│   │
│   ├── models/
│   │   ├── fraud/
│   │   │   ├── train.py                     # XGBoost + GNN fraud model
│   │   │   └── evaluate.py
│   │   ├── credit/
│   │   │   ├── train.py                     # Credit scoring + SHAP
│   │   │   └── evaluate.py
│   │   ├── churn/
│   │   │   ├── train.py                     # Customer churn prediction
│   │   │   └── evaluate.py
│   │   └── recommendations/
│   │       └── train.py                     # Collaborative filtering
│   │
│   ├── pipelines/
│   │   ├── fraud_training_pipeline.py
│   │   ├── credit_training_pipeline.py
│   │   ├── churn_training_pipeline.py
│   │   └── batch_scoring_pipeline.py        # Nightly batch scoring
│   │
│   ├── deployment/
│   │   ├── online_endpoint.py               # AML Managed Online Endpoint
│   │   ├── aks_deployment.py                # AKS deployment helper
│   │   └── batch_endpoint.py
│   │
│   └── utils/
│       ├── keyvault_client.py               # Key Vault secret retrieval
│       ├── logger.py                        # App Insights logger
│       └── config.py
│
├── api/
│   ├── app.py                               # FastAPI inference server
│   ├── routers/
│   │   ├── fraud.py                         # /v1/fraud/score
│   │   ├── credit.py                        # /v1/credit/score
│   │   ├── churn.py                         # /v1/churn/predict
│   │   ├── customer.py                      # /v1/customer/{id}/profile
│   │   └── recommendations.py              # /v1/recommend/{id}
│   ├── schemas.py                           # Pydantic request/response models
│   └── Dockerfile
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── hpa.yaml
│   └── ingress.yaml
│
├── notebooks/
│   ├── 01_eda_customer_data.ipynb
│   ├── 02_fraud_model_experiments.ipynb
│   ├── 03_credit_scoring_shap.ipynb
│   └── 04_churn_feature_engineering.ipynb
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── data_validation/
│
├── configs/
│   ├── fraud_model_config.yaml
│   ├── credit_model_config.yaml
│   ├── aml_config.yaml
│   └── logging_config.yaml
│
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
```

---

## 🤖 AI Integration — Banking Use Cases

The following AI modules are deployed as independent ML services on AKS, each serving a distinct banking function with real-time and batch inference modes.

### 1. 🛡️ Fraud Detection
Real-time transaction scoring using gradient boosting and graph neural networks. Flags card-not-present fraud, account takeovers, and structured transaction anomalies within a single inference call.

- **Latency target:** < 80ms P95
- **Model:** XGBoost + Graph Neural Network ensemble
- **Inference mode:** Real-time (AKS) + Batch nightly sweep

### 2. 📊 Credit Risk Scoring
ML-powered credit decisioning combining transactional behaviour, account history, and bureau data. Produces risk scores with SHAP value breakdowns for regulatory explainability.

- **Output:** Risk score + feature importance (SHAP)
- **Compliance:** Explainable decisions for RBI / Basel III requirements
- **Audit trail:** All decisions logged immutably to ADLS Gen2

### 3. 👤 Customer Churn Prediction
Identifies customers at risk of leaving using engagement signals, product usage patterns, and lifecycle stage features. Triggers proactive retention campaigns via Azure Logic Apps.

- **Prediction horizon:** 30-day forward churn probability
- **Integration:** Azure Logic Apps → CRM campaign trigger
- **Features:** 40+ behavioural and transactional signals

### 4. 💡 Product Recommendations
Collaborative filtering and content-based models surface relevant banking products — savings accounts, loans, FDs, insurance — personalised to each customer's financial profile and life events.

- **Customer view:** 360° profile from unified feature store
- **Channels:** Mobile app, web banking, relationship manager dashboard

### 5. 🔍 AML / Compliance Monitoring
Anti-money laundering model monitors transaction networks for structuring, layering, and integration patterns. Auto-generates Suspicious Activity Report (SAR) drafts with supporting evidence chains.

- **Model type:** Graph-based anomaly detection
- **Output:** Risk tier + SAR auto-draft (via Azure OpenAI)
- **Regulator ready:** Immutable audit log with full lineage

### 6. 🤝 AI Banker Assistant
LLM-powered internal assistant for relationship managers. Retrieves customer 360 summaries, flags risk signals, drafts communication templates, and answers product queries using Azure OpenAI Service (GPT-4o).

- **Integration:** Azure OpenAI Service (GPT-4o)
- **RAG source:** Customer feature store + product knowledge base
- **Access:** Internal web app + Teams bot integration

> **How AI transforms bank operations:** AI integration reduces manual review burden on fraud and compliance teams by automating first-pass triage, improves credit decision consistency, and enables personalised banking at scale. All models produce audit-ready evidence trails, reducing compliance overhead while improving detection across financial crime typologies.

---

## 👤 Customer Intelligence Module

The customer intelligence layer aggregates data from core banking, CRM, and digital channels into a unified AML Feature Store, powering all downstream ML models.

| Entity | Source | Update Frequency | Primary Use |
|---|---|---|---|
| Customer profile | Core banking + CRM | Real-time CDC | Churn, recommendations, AML |
| Transaction history | Payment processor | Real-time stream | Fraud, AML, credit scoring |
| Account details | Core banking ledger | Daily batch | Credit risk, product fit |
| KYC / onboarding | Digital onboarding app | Event-driven | Compliance, risk scoring |
| Behavioural signals | App/web clickstream | Near real-time | Churn, engagement |
| Bureau data | Credit bureau API | On demand (pull) | Credit underwriting |

```python
# src/data/feature_store.py
from azure.ai.ml import MLClient
from azure.ai.ml.entities import FeatureStore, FeatureSet
from azure.identity import DefaultAzureCredential

ml_client = MLClient(DefaultAzureCredential(), subscription_id="<sub-id>",
                     resource_group_name="rg-bankcore-dev",
                     workspace_name="aml-bankcore-dev")

# Customer 360 feature set definition
customer_features = FeatureSet(
    name="customer_360",
    version="2",
    features=[
        "avg_monthly_balance", "txn_velocity_7d",
        "product_count", "days_since_login",
        "credit_utilization", "kyc_score",
        "churn_risk_score", "lifetime_value_segment"
    ],
    source="azureml://datastores/adls_datastore/paths/curated/customers/"
)
ml_client.feature_sets.create_or_update(customer_features)
```

---

## ⚙️ Azure Tech Stack

| Layer | Service / Tool | Purpose |
|---|---|---|
| Source control | Azure DevOps Repos / GitHub | Versioned code, branch policies |
| CI/CD | Azure DevOps Pipelines | Automated build, test, deploy |
| ML platform | Azure Machine Learning | Training, tracking, registry |
| Experiment tracking | MLflow on AML | Metrics, params, artifacts per run |
| Data storage | ADLS Gen2 | Raw / processed / curated zones |
| ETL | Azure Data Factory | Ingestion, transformation, lineage |
| Feature store | AML Feature Store | Shared, versioned feature sets |
| Containerisation | Docker → ACR | Reproducible inference images |
| Serving (online) | AKS + AML Managed Endpoint | Real-time, autoscaled inference |
| Serving (batch) | AML Batch Endpoint | Nightly scoring runs |
| LLM integration | Azure OpenAI Service (GPT-4o) | AI banker assistant, SAR drafts |
| Monitoring | Azure Monitor + App Insights | Latency, drift, error alerts |
| Secret management | Azure Key Vault | All credentials at runtime |
| IaC | Azure Bicep | Reproducible infra provisioning |
| Identity | Azure AD + Managed Identity | Zero-credential architecture |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Azure CLI — `az extension add -n ml`
- Docker
- `kubectl`
- Make (optional)

### 1. Clone the repository
```bash
git clone https://dev.azure.com/your-org/bankcore-mlops/_git/bankcore-mlops
cd bankcore-mlops
```

### 2. Azure login & subscription
```bash
az login
az account set --subscription "<your-subscription-id>"
```

### 3. Provision Azure infrastructure
```bash
az deployment group create \
  --resource-group rg-bankcore-dev \
  --template-file infra/main.bicep \
  --parameters infra/parameters/dev.parameters.json
```
Provisions: AML Workspace, ADLS Gen2, ACR, AKS, Key Vault, App Insights, Azure OpenAI, Log Analytics.

### 4. Set up Python environment
```bash
python -m venv .venv
source .venv/bin/activate       # Linux/macOS
.venv\Scripts\activate          # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 5. Configure environment variables
```bash
cp .env.example .env

# .env — non-secret config only
AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_RESOURCE_GROUP=rg-bankcore-dev
AZURE_ML_WORKSPACE=aml-bankcore-dev
AZURE_STORAGE_ACCOUNT=sadlsbankcoredev
AZURE_KEY_VAULT_NAME=kv-bankcore-dev
AZURE_ACR_NAME=acrbankcore
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```
> Secrets (keys, connection strings, API keys) are **never** stored in `.env`. They are retrieved from Azure Key Vault at runtime via Managed Identity.

### 6. Submit a training job
```bash
# Fraud detection model
az ml job create \
  --file src/pipelines/fraud_training_pipeline.yml \
  --workspace-name aml-bankcore-dev \
  --resource-group rg-bankcore-dev
```

### 7. Deploy to AKS
```bash
az aks get-credentials --resource-group rg-bankcore-dev --name aks-bankcore-dev

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml

kubectl get pods -n bankcore
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/v1/fraud/score` | Real-time transaction fraud scoring |
| POST | `/v1/credit/score` | Credit risk assessment with SHAP |
| GET | `/v1/customer/{id}/profile` | Customer 360 enriched profile |
| POST | `/v1/churn/predict` | Churn probability + retention signals |
| GET | `/v1/recommend/{id}` | Personalised product recommendations |
| POST | `/v1/aml/flag` | AML transaction network check |
| GET | `/health` | Liveness + readiness probe |
| GET | `/metrics` | Prometheus-format metrics |
| GET | `/model/info` | Active model versions + metadata |

---

## 🔄 CI/CD — Azure DevOps Pipeline

```
Developer pushes to feature branch
         │
         ▼
┌─────────────────────────────────────────┐
│  CI Pipeline                             │
│  • Lint: flake8, black, isort           │
│  • Type check: mypy                     │
│  • Unit + integration tests (pytest)    │
│  • Data schema validation               │
│  • Docker build + push to ACR           │
│  • AML environment registration         │
└──────────────────┬──────────────────────┘
                   │  (on PR merge to main)
                   ▼
┌─────────────────────────────────────────┐
│  CD Pipeline                             │
│  • Trigger AML Training Pipeline        │
│  • Evaluate challenger vs champion      │
│  • Fairness + bias checks               │
│  • Register model in AML Registry       │
│  • Deploy to AKS staging namespace      │
│  • Smoke tests on staging               │
│  • Manual approval gate                 │
│  • Blue/Green deploy to AKS prod        │
└─────────────────────────────────────────┘
```

> Azure DevOps variable groups (linked to Key Vault) inject secrets at pipeline runtime — no secrets in YAML files.

---

## 📊 Experiment Tracking — AML + MLflow

```python
import mlflow
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient(DefaultAzureCredential(), "<sub-id>", "rg-bankcore-dev", "aml-bankcore-dev")
mlflow.set_tracking_uri(ml_client.workspaces.get("aml-bankcore-dev").mlflow_tracking_uri)
mlflow.set_experiment("fraud_detection_v2")

with mlflow.start_run():
    mlflow.log_param("model_type", "xgboost_gnn_ensemble")
    mlflow.log_metric("auc", 0.974)
    mlflow.log_metric("ks_statistic", 0.68)
    mlflow.log_metric("precision_at_top5pct", 0.89)
    mlflow.sklearn.log_model(model, "fraud_model")
```

**Logged per run:** hyperparameters, AUC / F1 / KS / Gini, SHAP plots, confusion matrices, data version, git SHA, environment hash.

---

## 📈 Monitoring & Alerts

| Signal | Tool | Threshold |
|---|---|---|
| Fraud model P95 latency | Application Insights | > 100ms → Warning |
| HTTP error rate | Application Insights | > 1% → Critical |
| Fraud feature drift | AML Data Drift Monitor | Score > 0.3 → Retrain |
| Credit model AUC degradation | AML Model Monitor | Drop > 0.02 → Alert |
| AKS node CPU | Azure Monitor for Containers | > 80% → Scale-out |
| Key Vault access anomaly | Microsoft Defender for Cloud | Any anomaly → Immediate |

---

## 🔐 Security & Identity

All service-to-service communication uses Azure Managed Identity — no hardcoded credentials anywhere in the codebase.

| Resource | Target | Role |
|---|---|---|
| AML Workspace | ADLS Gen2 | Storage Blob Data Contributor |
| AML Workspace | ACR | AcrPull (Managed Identity) |
| AKS | ACR | AcrPull (AKS Identity) |
| App | Key Vault | Key Vault Secrets User |
| DevOps Pipeline | Azure | Service Principal (scoped RBAC) |
| Banking APIs | Backend services | Azure API Management + OAuth2 |

> **Regulatory compliance:** All prediction logs and data lineage are retained with immutable audit trails (WORM policy on ADLS Gen2). SHAP explanations are stored per credit decision for RBI / Basel III explainability requirements.

---

## 🛠️ Makefile Commands

```bash
make install          # Install all dependencies
make az-login         # Azure CLI login + subscription
make infra-deploy     # Deploy Bicep infra to dev
make train-fraud      # Submit fraud detection training job
make train-credit     # Submit credit scoring training job
make evaluate         # Run model evaluation script
make acr-build        # Build & push Docker image to ACR
make aks-deploy       # Apply k8s manifests to AKS
make endpoint-deploy  # Deploy AML Managed Online Endpoint
make test             # Run all tests
make lint             # Lint & format check
make format           # Auto-format (black + isort)
make clean            # Remove cache and temp files
```

---

## 🧪 Running Tests

```bash
# All tests
make test

# Unit tests
pytest tests/unit/ -v

# Integration tests (requires Azure credentials)
pytest tests/integration/ -v --azure

# Data validation
pytest tests/data_validation/ -v

# Coverage report
pytest --cov=src --cov-report=html
```

---

## 🤝 Contributing

1. Clone the Azure DevOps repo and create a branch (`feature/your-feature`)
2. Make changes and add tests
3. Run `make lint && make test`
4. Push and open a Pull Request in Azure DevOps
5. CI pipeline runs automatically on PR
6. After approval, merge triggers CD pipeline

Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

| Name | Role | Contact |
|---|---|---|
| Your Name | ML Engineer | your.email@bank.com |
| Your Name | MLOps Engineer | your.email@bank.com |

---

> *"Azure ML + AKS + AI — the enterprise backbone for banking intelligence that ships safely, scales reliably, and stays auditable."*
