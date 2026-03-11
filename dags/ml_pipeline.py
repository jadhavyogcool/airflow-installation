from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os

DATA_PATH = "/opt/airflow/dags/data"

def download_data():
    
    os.makedirs(DATA_PATH, exist_ok=True)

    iris = load_iris()

    df = pd.DataFrame(
        iris.data,
        columns=iris.feature_names
    )

    df["target"] = iris.target

    df.to_csv(f"{DATA_PATH}/iris_raw.csv", index=False)

    print("Dataset downloaded and saved")


def clean_data():

    df = pd.read_csv(f"{DATA_PATH}/iris_raw.csv")

    df = df.dropna()

    df.to_csv(f"{DATA_PATH}/iris_clean.csv", index=False)

    print("Data cleaned and saved")


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

    print(f"Model Accuracy: {accuracy}")


with DAG(
    dag_id="ml_training_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    download_task = PythonOperator(
        task_id="download_data",
        python_callable=download_data
    )

    clean_task = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data
    )

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=train_model
    )

    download_task >> clean_task >> train_task