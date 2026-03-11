from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task1():
    print("Task 1 Executed")

def task2():
    print("Task 2 Executed")

def task3():
    print("Task 3 Executed")

with DAG(
    dag_id="simple_airflow_pipeline",
    start_date=datetime(2024,1,1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="task_1",
        python_callable=task1
    )

    t2 = PythonOperator(
        task_id="task_2",
        python_callable=task2
    )

    t3 = PythonOperator(
        task_id="task_3",
        python_callable=task3
    )

    t1 >> t2 >> t3
