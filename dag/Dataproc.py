from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator, DataprocDeleteClusterOperator, DataprocSubmitJobOperator
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup

from google.cloud import dataproc_v1

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

# Define the DAG
with DAG(
    'dataproc_example_dag',
    default_args=default_args,
    description='A simple DAG to create a Dataproc cluster, run a job, and delete the cluster',
    schedule_interval=None,  # Set to None for manual execution
    catchup=False,
) as dag:

    # Define the cluster configuration
    cluster_config = {
        "project_id": "your-gcp-project-id",
        "cluster_name": "your-cluster-name",
        "config": {
            "config": {
                "gce_cluster_config": {
                    "zone_uri": "us-central1-a",
                },
                "master_config": {
                    "num_instances": 1,
                    "machine_type_uri": "n1-standard-1",
                },
                "worker_config": {
                    "num_instances": 2,
                    "machine_type_uri": "n1-standard-1",
                },
            }
        },
    }

    # Task to create Dataproc cluster
    create_cluster = DataprocCreateClusterOperator(
        task_id='create_dataproc_cluster',
        project_id=cluster_config["project_id"],
        cluster_name=cluster_config["cluster_name"],
        cluster_config=cluster_config["config"],
    )

    # Define the job configuration
    job_config = {
        "reference": {"project_id": cluster_config["project_id"]},
        "placement": {"cluster_name": cluster_config["cluster_name"]},
        "hadoop_job": {
            "main_jar_file_uri": "gs://your-bucket/path/to/your-jar-file.jar",
            "args": ["arg1", "arg2"],
        },
    }

    # Task to submit a job to Dataproc cluster
    submit_job = DataprocSubmitJobOperator(
        task_id='submit_dataproc_job',
        project_id=cluster_config["project_id"],
        region="us-central1",
        job=job_config,
    )

    # Task to delete Dataproc cluster
    delete_cluster = DataprocDeleteClusterOperator(
        task_id='delete_dataproc_cluster',
        project_id=cluster_config["project_id"],
        cluster_name=cluster_config["cluster_name"],
        region="us-central1",
    )

    # Set up task dependencies
    create_cluster >> submit_job >> delete_cluster
