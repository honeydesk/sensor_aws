from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

from sensor.entity.config_entity import BatchPredictionConfig
from sensor.pipeline.batch_prediction import BatchPrediction

batch_config = BatchPredictionConfig()


with DAG(
    'batch_prediction',
    default_args={'retries': 2},
    # [END default_args]
    description='Sensor Fault Detection',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2023, 3, 29, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:
    
    def download_files(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync s3://{bucket_name}/inbox {batch_config.inbox_dir}")

    def batch_prediction(**kwargs):
        batch_pred = BatchPrediction(batch_config=batch_config)
        batch_pred.start_prediction()
        
    def upload_prediction_files(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        #upload prediction folder to predictionfiles folder in s3 bucket
        os.system(f"aws s3 sync {batch_config.archive_dir} s3://{bucket_name}/archive")
        os.system(f"aws s3 sync {batch_config.outbox_dir} s3://{bucket_name}/outbox")
    


    download_files_task = PythonOperator(
            task_id="download_files",
            python_callable=download_files

    )

    batch_prediction_files_task = PythonOperator(
            task_id="batch_prediction",
            python_callable=batch_prediction

    )

    upload_prediction_files_task = PythonOperator(
            task_id="upload_prediction_files",
            python_callable=upload_prediction_files

    )

    download_files_task >> batch_prediction_files_task >> upload_prediction_files_task