
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

Code:

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task1():
    print("Task 1 executed")

def task2():
    print("Task 2 executed")

def task3():
    print("Task 3 executed")

with DAG(
    dag_id="simple_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="task1", python_callable=task1)
    t2 = PythonOperator(task_id="task2", python_callable=task2)
    t3 = PythonOperator(task_id="task3", python_callable=task3)

    t1 >> t2 >> t3

Pipeline:

task1 → task2 → task3

---

# Machine Learning Pipeline DAG

Create:

dags/ml_pipeline.py

Code:

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os

DATA_PATH="/opt/airflow/dags/data"

def download_data():
    os.makedirs(DATA_PATH, exist_ok=True)
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df["target"] = iris.target
    df.to_csv(f"{DATA_PATH}/iris_raw.csv", index=False)

def clean_data():
    df = pd.read_csv(f"{DATA_PATH}/iris_raw.csv")
    df = df.dropna()
    df.to_csv(f"{DATA_PATH}/iris_clean.csv", index=False)

def train_model():
    df = pd.read_csv(f"{DATA_PATH}/iris_clean.csv")
    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression()
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print("Model Accuracy:", accuracy)

with DAG(
    dag_id="ml_training_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    download_task = PythonOperator(task_id="download_data", python_callable=download_data)
    clean_task = PythonOperator(task_id="clean_data", python_callable=clean_data)
    train_task = PythonOperator(task_id="train_model", python_callable=train_model)

    download_task >> clean_task >> train_task

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

Model Accuracy: 0.97

---

# Stop Airflow

CTRL + C

docker compose down

---

# Learning Outcomes

Students will learn:

• DAG concepts
• Workflow orchestration
• Task dependencies
• Data pipelines
• ML pipeline automation
