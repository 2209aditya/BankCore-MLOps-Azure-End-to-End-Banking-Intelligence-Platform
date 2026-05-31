# MLOps-Project-Azure-End-to-End-Machine-Learning-Pipelin# 🚀 MLOps Project — Azure End-to-End Machine Learning Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Azure ML](https://img.shields.io/badge/Azure_ML-Workspace-0078D4?logo=microsoftazure)
![Azure DevOps](https://img.shields.io/badge/Azure_DevOps-CI%2FCD-0078D7?logo=azuredevops)
![AKS](https://img.shields.io/badge/AKS-Kubernetes-326CE5?logo=kubernetes)
![Docker](https://img.shields.io/badge/Docker-ACR-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Overview

A production-grade **MLOps pipeline on Microsoft Azure** covering the full machine learning lifecycle — from data ingestion on **Azure Data Lake Storage (ADLS Gen2)** and model training on **Azure Machine Learning**, to containerized deployment on **Azure Kubernetes Service (AKS)** and monitoring via **Azure Monitor + Application Insights**.

Built for reproducibility, scalability, and enterprise-grade observability using native Azure services.

---

## 🏗️ Azure Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          AZURE SUBSCRIPTION                              │
│                                                                          │
│  ┌──────────────────────┐     ┌──────────────────────────────────────┐  │
│  │  Data Layer           │     │  ML Platform                         │  │
│  │  ─────────────────── │     │  ─────────────────────────────────── │  │
│  │  ADLS Gen2            │────▶│  Azure Machine Learning Workspace    │  │
│  │  (raw / processed /   │     │  • Compute Clusters (training)       │  │
│  │   curated zones)      │     │  • Compute Instances (notebooks)     │  │
│  │                       │     │  • Managed Environments              │  │
│  │  Azure Data Factory   │     │  • MLflow Experiment Tracking        │  │
│  │  (ingestion / ETL)    │     │  • Model Registry                    │  │
│  └──────────────────────┘     └──────────────┬───────────────────────┘  │
│                                               │                          │
│  ┌──────────────────────┐     ┌──────────────▼───────────────────────┐  │
│  │  CI/CD               │     │  Serving Layer                        │  │
│  │  ─────────────────── │     │  ─────────────────────────────────── │  │
│  │  Azure DevOps        │────▶│  Azure Kubernetes Service (AKS)      │  │
│  │  • Pipelines (CI/CD) │     │  • Real-time inference pods          │  │
│  │  • Repos (Git)       │     │  • Horizontal Pod Autoscaler         │  │
│  │  • Artifacts         │     │                                       │  │
│  │                       │     │  Azure Container Registry (ACR)      │  │
│  │  Azure Container     │     │  (Docker image storage)               │  │
│  │  Registry (ACR)      │     └──────────────┬───────────────────────┘  │
│  └──────────────────────┘                    │                          │
│                                               │                          │
│  ┌──────────────────────────────────────────▼───────────────────────┐  │
│  │  Monitoring & Security                                             │  │
│  │  Azure Monitor • Application Insights • Azure Key Vault           │  │
│  │  Log Analytics Workspace • Microsoft Defender for Cloud           │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
mlops-project/
├── .azure/
│   └── pipelines/
│       ├── ci-pipeline.yml             # Azure DevOps CI pipeline
│       ├── cd-pipeline.yml             # Azure DevOps CD pipeline
│       └── training-pipeline.yml       # AML training pipeline trigger
│
├── infra/
│   ├── main.bicep                      # Azure Bicep — root deployment
│   ├── modules/
│   │   ├── aml_workspace.bicep         # Azure ML Workspace
│   │   ├── storage_adls.bicep          # ADLS Gen2 + containers
│   │   ├── aks_cluster.bicep           # AKS cluster definition
│   │   ├── acr.bicep                   # Azure Container Registry
│   │   ├── keyvault.bicep              # Azure Key Vault
│   │   └── monitor.bicep               # Log Analytics + App Insights
│   └── parameters/
│       ├── dev.parameters.json
│       ├── staging.parameters.json
│       └── prod.parameters.json
│
├── data/
│   ├── raw/                            # Mirrors ADLS raw zone
│   ├── processed/                      # Mirrors ADLS processed zone
│   └── schemas/                        # JSON/Avro schema definitions
│
├── notebooks/
│   ├── 01_eda.ipynb                    # Run on AML Compute Instance
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── src/
│   ├── data/
│   │   ├── adls_connector.py           # ADLS Gen2 read/write (azure-storage-blob)
│   │   ├── adf_trigger.py              # Trigger Azure Data Factory pipelines
│   │   ├── validation.py               # Data quality checks
│   │   └── preprocessing.py            # Feature engineering
│   │
│   ├── models/
│   │   ├── train.py                    # AML training script
│   │   ├── evaluate.py                 # Evaluation & metric logging to AML
│   │   └── predict.py                  # Inference logic
│   │
│   ├── pipelines/
│   │   ├── aml_training_pipeline.py    # Azure ML Pipeline (ComponentJob)
│   │   └── aml_batch_pipeline.py       # AML Batch Endpoint pipeline
│   │
│   ├── deployment/
│   │   ├── online_endpoint.py          # AML Managed Online Endpoint
│   │   ├── aks_deployment.py           # AKS deployment manifest helper
│   │   └── batch_endpoint.py           # AML Batch Endpoint
│   │
│   └── utils/
│       ├── keyvault_client.py          # Azure Key Vault secret retrieval
│       ├── logger.py                   # Azure Monitor / App Insights logger
│       └── config.py                   # Config loader
│
├── api/
│   ├── app.py                          # FastAPI inference server
│   ├── schemas.py                      # Pydantic request/response models
│   └── Dockerfile                      # Container image (pushed to ACR)
│
├── k8s/
│   ├── deployment.yaml                 # AKS Deployment manifest
│   ├── service.yaml                    # AKS Service (LoadBalancer)
│   ├── hpa.yaml                        # Horizontal Pod Autoscaler
│   └── ingress.yaml                    # Azure Application Gateway Ingress
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── data_validation/
│
├── configs/
│   ├── model_config.yaml               # Hyperparameters & model settings
│   ├── aml_config.yaml                 # Azure ML workspace config
│   ├── data_config.yaml                # ADLS paths & schema
│   └── logging_config.yaml
│
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── setup.py
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
└── README.md
```

---

## ⚙️ Azure Tech Stack

| Layer | Azure Service / Tool |
|---|---|
| **Source Control** | Azure DevOps Repos / GitHub |
| **CI/CD** | Azure DevOps Pipelines |
| **ML Platform** | Azure Machine Learning (AML) |
| **Experiment Tracking** | MLflow on AML Workspace |
| **Model Registry** | AML Model Registry |
| **Data Storage** | Azure Data Lake Storage Gen2 (ADLS) |
| **Data Ingestion / ETL** | Azure Data Factory (ADF) |
| **Feature Engineering** | Azure Databricks (optional) |
| **Training Compute** | AML Compute Clusters (CPU/GPU) |
| **Containerization** | Docker → Azure Container Registry (ACR) |
| **Model Serving (Online)** | AML Managed Online Endpoint / AKS |
| **Model Serving (Batch)** | AML Batch Endpoint |
| **Orchestration** | Azure ML Pipelines (ComponentJobs) |
| **Secret Management** | Azure Key Vault |
| **Monitoring** | Azure Monitor + Application Insights |
| **Log Analytics** | Azure Log Analytics Workspace |
| **IaC** | Azure Bicep / ARM Templates |
| **Identity & Access** | Azure Active Directory + Managed Identity |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Azure CLI (`az`) — [Install guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- Azure ML CLI extension — `az extension add -n ml`
- Docker
- kubectl (for AKS deployments)
- Make (optional)

### 1. Clone the Repository

```bash
git clone https://dev.azure.com/your-org/mlops-project/_git/mlops-project
cd mlops-project
```

### 2. Azure Login & Set Subscription

```bash
az login
az account set --subscription "<your-subscription-id>"
```

### 3. Provision Azure Infrastructure (Bicep)

```bash
# Deploy to dev environment
az deployment group create \
  --resource-group rg-mlops-dev \
  --template-file infra/main.bicep \
  --parameters infra/parameters/dev.parameters.json
```

This provisions: AML Workspace, ADLS Gen2, ACR, AKS, Key Vault, App Insights, Log Analytics.

### 4. Set Up Python Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 5. Configure Environment Variables

```bash
cp .env.example .env
```

```env
# .env
AZURE_SUBSCRIPTION_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
AZURE_RESOURCE_GROUP=rg-mlops-dev
AZURE_ML_WORKSPACE=aml-mlops-dev
AZURE_STORAGE_ACCOUNT=sadlsmlopsdev
AZURE_KEY_VAULT_NAME=kv-mlops-dev
AZURE_ACR_NAME=acrmlopsdev
AZURE_TENANT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Secrets (keys, connection strings) are **never stored in `.env`** — they are retrieved from **Azure Key Vault** at runtime via Managed Identity.

### 6. Connect to AML Workspace

```bash
az ml workspace show \
  --name aml-mlops-dev \
  --resource-group rg-mlops-dev
```

### 7. Submit a Training Job

```bash
# Submit AML training pipeline
az ml job create \
  --file src/pipelines/aml_training_pipeline.yml \
  --workspace-name aml-mlops-dev \
  --resource-group rg-mlops-dev

# Or via Python SDK v2
python src/pipelines/aml_training_pipeline.py
```

---

## 📊 Experiment Tracking — Azure ML + MLflow

All training runs are tracked in the **AML Workspace MLflow integration**:

```python
import mlflow
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="<sub-id>",
    resource_group_name="rg-mlops-dev",
    workspace_name="aml-mlops-dev"
)

mlflow.set_tracking_uri(ml_client.workspaces.get("aml-mlops-dev").mlflow_tracking_uri)
mlflow.set_experiment("customer_churn_prediction")

with mlflow.start_run():
    mlflow.log_param("n_estimators", 300)
    mlflow.log_metric("auc", 0.91)
    mlflow.sklearn.log_model(model, "model")
```

**Access the MLflow UI** → Azure ML Studio → Experiments tab.

Logged per run:
- Hyperparameters & configs
- Metrics (Accuracy, F1, AUC, RMSE)
- Model artifacts (weights, plots, feature importance)
- Tags (git SHA, AML run ID, dataset version, environment)

---

## 🐳 Container Build & Push to ACR

```bash
# Login to Azure Container Registry
az acr login --name acrmlopsdev

# Build and push Docker image
docker build -t acrmlopsdev.azurecr.io/mlops-api:latest ./api
docker push acrmlopsdev.azurecr.io/mlops-api:latest

# Or use ACR Tasks (build in the cloud)
az acr build \
  --registry acrmlopsdev \
  --image mlops-api:latest \
  ./api
```

---

## ☸️ AKS Deployment

```bash
# Get AKS credentials
az aks get-credentials \
  --resource-group rg-mlops-dev \
  --name aks-mlops-dev

# Deploy to AKS
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n mlops
kubectl get svc -n mlops
```

### AKS API Endpoints

```
POST /predict          → Single prediction
POST /predict/batch    → Batch predictions
GET  /health           → Health check
GET  /model/info       → Active model metadata
GET  /metrics          → Prometheus-format metrics (scraped by Azure Monitor)
```

---

## 🤖 AML Managed Online Endpoint (Alternative to AKS)

```bash
# Create managed online endpoint
az ml online-endpoint create \
  --name mlops-endpoint-dev \
  --workspace-name aml-mlops-dev \
  --resource-group rg-mlops-dev

# Deploy model to endpoint
az ml online-deployment create \
  --name blue \
  --endpoint mlops-endpoint-dev \
  --file src/deployment/online_endpoint.yml \
  --workspace-name aml-mlops-dev \
  --resource-group rg-mlops-dev \
  --all-traffic
```

---

## 🔄 CI/CD — Azure DevOps Pipelines

```
Developer pushes to feature branch (Azure Repos / GitHub)
        │
        ▼
   ┌──────────────────────────────────────────┐
   │  CI Pipeline (azure-pipelines.yml)        │
   │  • Lint: flake8, black, isort            │
   │  • Type check: mypy                       │
   │  • Unit & integration tests (pytest)      │
   │  • Data schema validation                 │
   │  • Docker build + push to ACR             │
   │  • AML environment registration           │
   └─────────────────────┬────────────────────┘
                         │  (on PR merge to main)
                         ▼
   ┌──────────────────────────────────────────┐
   │  CD Pipeline                              │
   │  • Trigger AML Training Pipeline          │
   │  • Evaluate model vs champion             │
   │  • Register model in AML Model Registry   │
   │  • Deploy to AKS staging namespace        │
   │  • Run smoke tests on staging             │
   │  • Manual approval gate → prod deploy     │
   │  • Blue/Green deployment on AKS prod      │
   └──────────────────────────────────────────┘
```

**Azure DevOps variable groups** (linked to Key Vault) are used to inject secrets at pipeline runtime — no secrets in YAML files.

---

## 📈 Monitoring — Azure Monitor & Application Insights

### What's Monitored

| Signal | Tool |
|---|---|
| Prediction latency & throughput | Application Insights |
| HTTP error rates (4xx / 5xx) | Application Insights |
| Data drift (input features) | AML Data Drift Monitor |
| Model performance degradation | AML Model Monitor |
| AKS node / pod health | Azure Monitor for Containers |
| Custom ML metrics | Azure Monitor custom metrics |
| Logs (training + inference) | Log Analytics Workspace |

### Alerts

Azure Monitor Alerts are configured for:
- P95 latency > 500ms → **Warning**
- Error rate > 1% → **Critical → PagerDuty**
- Data drift score > 0.3 → **Retrain trigger**
- AKS node CPU > 80% → **Scale-out**

### AML Data Drift Monitor

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import DataDriftMonitor

monitor = DataDriftMonitor(
    name="churn-model-monitor",
    target_dataset="inference-dataset",
    baseline_dataset="training-dataset",
    frequency="Day",
    alert_settings={"email_addresses": ["mlteam@org.com"]}
)
ml_client.monitors.create_or_update(monitor)
```

---

## 🔐 Security & Identity

All service-to-service communication uses **Azure Managed Identity** — no hardcoded credentials anywhere.

| Resource | Access |
|---|---|
| AML Workspace → ADLS | Managed Identity (Storage Blob Data Contributor) |
| AML Workspace → ACR | Managed Identity (AcrPull) |
| AKS → ACR | AKS Managed Identity (AcrPull) |
| App → Key Vault | Managed Identity (Key Vault Secrets User) |
| DevOps Pipeline → Azure | Service Principal (scoped RBAC) |

Secrets rotation is handled via **Key Vault** with automated rotation policies.

---

## 🗃️ Data Versioning — ADLS + AML Datasets

```bash
# Register a new dataset version in AML
az ml data create \
  --name customer-churn-dataset \
  --version 3 \
  --path azureml://datastores/adls_datastore/paths/processed/churn/v3/ \
  --type uri_folder \
  --workspace-name aml-mlops-dev \
  --resource-group rg-mlops-dev
```

ADLS Gen2 zones:
- `raw/` — immutable ingested data
- `processed/` — cleaned & feature-engineered
- `curated/` — ML-ready, versioned datasets

---

## 🛠️ Makefile Commands

```bash
make install          # Install all dependencies
make az-login         # Azure CLI login + set subscription
make infra-deploy     # Deploy Bicep infra to dev
make train            # Submit AML training job
make evaluate         # Run model evaluation script
make acr-build        # Build & push Docker image to ACR
make aks-deploy       # Apply k8s manifests to AKS
make endpoint-deploy  # Deploy to AML Managed Online Endpoint
make test             # Run all tests
make lint             # Lint & format check
make format           # Auto-format (black + isort)
make clean            # Remove cache and temp files
```

---

## 📁 AML Configuration

```yaml
# configs/aml_config.yaml
azure:
  subscription_id: "${AZURE_SUBSCRIPTION_ID}"
  resource_group: "rg-mlops-dev"
  workspace_name: "aml-mlops-dev"
  location: "eastus2"

compute:
  training_cluster: "cpu-cluster-d4sv3"
  gpu_cluster: "gpu-cluster-nc6s"
  instance_type: "Standard_D4s_v3"
  min_instances: 0
  max_instances: 10

datastore:
  name: "adls_datastore"
  account_name: "sadlsmlopsdev"
  container_name: "mldata"

model:
  name: "customer_churn_xgboost"
  experiment_name: "customer_churn_prediction"
  environment_name: "mlops-training-env"
  environment_version: "3"

deployment:
  endpoint_name: "mlops-endpoint-dev"
  deployment_name: "blue"
  instance_type: "Standard_DS3_v2"
  instance_count: 2
```

---

## 🧪 Running Tests

```bash
# Run all tests
make test

# Unit tests
pytest tests/unit/ -v

# Integration tests (requires Azure credentials)
pytest tests/integration/ -v --azure

# Coverage report
pytest --cov=src --cov-report=html
```

---

## 🤝 Contributing

1. Clone the Azure DevOps repo and create a branch (`feature/your-feature`)
2. Make changes and add tests
3. Run `make lint && make test`
4. Push and open a **Pull Request** in Azure DevOps
5. CI pipeline runs automatically on PR
6. After approval, merge triggers CD pipeline

Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

| Name | Role | Contact |
|---|---|---|
| Your Name | ML Engineer | your.email@org.com |
| Your Name | MLOps Engineer | your.email@org.com |

---

> **"Azure ML + AKS + DevOps — the enterprise backbone for shipping models that actually run in production."**
