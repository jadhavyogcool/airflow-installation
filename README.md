
# Apache Airflow Docker Setup with Simple DAG and ML Pipeline

## Overview
This guide explains how to run Apache Airflow using Docker Compose and execute two example workflows:

1. Simple DAG
2. Machine Learning Pipeline
   - Download Data
   - Clean Data
   - Train Model

This setup is useful for teaching Data Engineering concepts like workflow orchestration, DAGs, and ML pipelines.

---

# Prerequisites

Install Docker Desktop:
https://www.docker.com/products/docker-desktop/

Verify installation:

docker --version
docker compose version

---

# Step 1: Create Project Folder

mkdir airflow-demo
cd airflow-demo

---

# Step 2: Download Official Airflow Docker Compose

curl -LfO https://airflow.apache.org/docs/apache-airflow/2.8.1/docker-compose.yaml

---

# Step 3: Create Required Directories

mkdir dags
mkdir logs
mkdir plugins
mkdir config
mkdir dags/data

Project structure:

airflow-demo/
 ├─ dags/
 │   ├─ simple_dag.py
 │   ├─ ml_pipeline.py
 │   └─ data/
 ├─ logs/
 ├─ plugins/
 ├─ config/
 ├─ docker-compose.yaml
 └─ .env

---

# Step 4: Create .env file

Create file:

.env

Add:

AIRFLOW_UID=50000

---

# Step 5: Update docker-compose.yaml

Airflow containers do not include ML libraries by default.

Find:

environment:
  &airflow-common-env

Add:

_PIP_ADDITIONAL_REQUIREMENTS: pandas scikit-learn

IMPORTANT:
Ensure _PIP_ADDITIONAL_REQUIREMENTS appears only once.

Example:

environment:
  &airflow-common-env
  AIRFLOW__CORE__EXECUTOR: CeleryExecutor
  _PIP_ADDITIONAL_REQUIREMENTS: pandas scikit-learn

---

# Step 6: Initialize Airflow

docker compose up airflow-init

---

# Step 7: Start Airflow

docker compose up

Containers started:

• airflow-webserver
• airflow-scheduler
• airflow-worker
• postgres
• redis

---

# Step 8: Open Airflow UI

http://localhost:8080

Login:

Username: airflow
Password: airflow

---

# Simple DAG Example

Create file:

dags/simple_dag.py

---

# Machine Learning Pipeline DAG

Create:

dags/ml_pipeline.py



Pipeline:

Download Data
↓
Clean Data
↓
Train Model

---

# Running the DAG

Enable DAGs:

simple_pipeline
ml_training_pipeline

Click Trigger DAG.

---

# View Model Accuracy

Graph View → train_model → Logs

Example:

Model Accuracy: --

---

# Stop Airflow

CTRL + C

docker compose down

---
