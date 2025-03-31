## Set Up and Reproducibility

### Environment Prerequisites

1. Create a [GCP account](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md) with your Google email address.
2. Set up a project and note the project id.
3. Make a Service Account and grant it the following roles:
    - Editor
    - BigQuery Admin
    - Compute Admin
    - Storage Admin
    - Storage Object Admin
    - Storage Object Creator
    - Storage Object Viewer
    - Dataproc Worker
    - Dataproc Service Agent
4. Enable the following APIs in the console:
    - https://console.cloud.google.com/apis/library/iam.googleapis.com
    - https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
    - https://console.developers.google.com/apis/api/dataproc.googleapis.com/
5. Follow the instructions in this [video](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) to set up a GCP Compute Engine Virtual Machine (VM) instance, which includes set up for Docker and Terraform as well.
6. SSH into your VM instance and [install the gcloud CLI](https://cloud.google.com/sdk/docs/install).
7. Using the gcloud CLI, [connect your project to the VM instance](https://cloud.google.com/compute/docs/connect/standard-ssh#gcloud).
8. Set up (or confirm the installation of) the following tools in your VM instance:
    - Terraform
    - Docker and Docker Compose
    - [Spark and PySpark](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/linux.md)


### Running the Code

1. Run the command below to clone this repository:
```bash
git clone https://github.com/gatechme99/nfl-datapipeline
```

2. Update the `/terraform/variables.tf` file to match your GCS variables.
    - Add GCS credentials, if necessary.
    - Update with your project name, location, and region.

3. Provision GCP resources using Terraform.
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

4. Spin up Kestra using Docker.
```bash
cd ..
docker compose up -d
```

- You may need to manually forward port 8080.
- Open a browser tab and navigate to `http://localhost:8080/`.

5. Create a Kaggle account.
    - Note your user name.
    - Under Settings, create a new API token.

6. In the Kestra UI:

    - Navigate to Flows.
    - Create a new flow by copying in the code from `gcp_kv.yaml`.
    - Save the file and xecute the DAG defined in `gcp_kv.yaml`.
    - Navigate to Namespaces. Select the appropriate namespace. Go to KV Store.
        - Add GCP_CREDS using the json for your service account.
        - Add your KAGGLE_USERNAME.
        - Add your KAGGLE_KEY (API token)
    
    <img src="/images/kestra_kv.png" alt="kestra_kv_store" width="75%">

    - Navigate back to Flows.
    - Create another new flow by copying in the code from `kaggle_gcs.yaml`.
    - Save the file and execute the DAG defined in `kaggle_gcs.yaml`.

    Navigate to your GCS bucket to confirm 13 CSV files were unzipped and uploaded from Kaggle.

    **NOTE:** If you have issues with Kestra dowloading the dataset from Kaggle and uploading into GCS, download the [zip file locally](https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/data), unzip the files, and upload the `games.csv`, `player_play.csv`, and `players.csv` files to your GCS bucket.

    <img src="/images/gcs_bucket.png" alt="gcs_bucket" width="50%">

    - Update `spark_bigquery.py` file. You may need to save this file locally.
    - Navigate back to Flows.
    - Create another new flow by copying in the code from `gcs_dataproc_pyspark.yaml`.
    - Save the file and execute the DAG defined in `gcs_dataproc_pyspark.yaml`, selecting `spark_bigquery.py` from the UI as the input file.

    Navigate to BigQuery and confirm the `total_qb_offense` table exists under the `zoomcamp` dataset. There should be 252 rows in the table.

    <img src="/images/bq_table.png" alt="final_table" width="50%">

7. Open Looker Studio and connect it to the `total_qb_offense` table in BigQuery.

8. Start your data exploration in Looker Studio.

9. When you are done, run the following to shut down Kestra and tear down the GCP resources:

```bash
docker compose down
terraform destroy
```

10. Shut down the VM instance in the GCP Console. You may want to confirm no other virtual machines are running (including Dataproc). You can also confirm resources were destroyed in GCS and BigQuery.