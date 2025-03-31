# NFL Data Engineering Project
Capstone project for the 2025 Cohort of the [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/README.md) presented by DataTalksClub. This final project highlights the fundamentals of data engineering by building an end-to-end data pipeline from scratch, using industry-standard tooling and best practices.

## Problem Statement
The regular season of the National Football League (NFL) consists of 272 games, with each of the NFL's 32 teams playing 17 games during an 18-week period with one "bye" week off. The quarterback is widely considered the most important position in the NFL due to their role as the leader of the offense, controlling the ball on nearly every play and making crucial decisions that directly impact the team's performance. 

A quarterback's age significantly impacts their performance, with peak performance generally occurring between 26 and 34, after which physical and mental abilities may decline, affecting arm strength, reflexes, and mobility. NFL injuries, particularly ligament sprains/tears, concussions, and fractures, can significantly impact player performance, leading to missed games, reduced effectiveness, and even career-ending injuries, with some players facing long-term health issues. 

Using data from weeks 1 through 9 of the 2022 NFL regular season, we want to explore:

   1. How age relates to total offensive yards produced.

   2. How age relates to offensive yards produced per game week.

Offensive yards are the sum of passing yards and rushing yards less yards lost when a quarterback is sacked (tackled behind the line of scrimmage) by the defense.

## Architecture
![End-to-end data pipeline architecture](/images/architecture.png)

### Cloud
- This project was built using modular cloud services on **[Google Cloud Platform (GCP)](https://cloud.google.com/)**. 
- **[Google Compute Engine (GCE)](https://cloud.google.com/products/compute)**, the infrastructure as a service (IaaS) component of GCP, was used to spin up virtual machines (VMs) on demand.
- **[GitHub](https://github.com/)** was used to create, store, manage, and share code, with **[Git](https://git-scm.com/)** providing distributed version control.
- **[Terraform](https://www.terraform.io/)** was used for automated cloud provisioning with declarative infrastructure as code (IaC) to create buckets in **[Google Cloud Storage (GCS)](https://cloud.google.com/storage)** and datasets in **[Google BigQuery](https://cloud.google.com/bigquery)**.
- **[Docker](https://www.docker.com/)** was used to package applications and their dependencies into a portable container for easy deployment and management, particularly **[Kestra](https://kestra.io/)** to orchestrate the end-to-end pipeline.

### Data Ingestion
The dataset used for this project came from the [NFL Big Data Bowl 2025](https://www.kaggle.com/competitions/nfl-big-data-bowl-2025/) challenge hosted by **[Kaggle](https://www.kaggle.com/)**. While the competition itself ended on January 6, 2025, the dataset is still available for download and analysis.

#### Batch/Workflow Orchestration
Kestra is used to execute the [`kaggle_gcs`](/kaggle_gcs.yaml) DAG.
- The [Kaggle API](https://github.com/Kaggle/kaggle-api) is called to download the zip file for the NFL Big Data Bowl 2025 dataset.
- The file is unzipped, and 13 CSV files are uploaded to a GCS bucket.

### Transformations & Data Warehouse
Kestra is then used execute the [`gcs_dataproc_pyspark`](/gcs_dataproc_pyspark.yaml) DAG.
- The code to transform the data resides in the PySpark job [`spark_bigquery.py`](/spark_bigquery.py). 
- The PySpark job is submitted to Google Cloud Dataproc which handles all the clusters needed for transformation.
- Data is partitioned and written to parquet files.
- The transformed data is loaded into BigQuery as a table.
- No clustering was performed because the dataset is relatively small, and thus, the benefits may not be as pronounced as with larger datasets.

### Dashboards
Visualization of the transformed data loaded into BigQuery as a table was created using Looker Studio. You can access the dashboards [here](https://lookerstudio.google.com/s/tB6SDPVdITo).

The first dashboard shows the distibution of total offensive yards by age.
![Dashboard comparing total offensive yards to age](/images/dashboard1.png)

The second dashboard shows the distibution of offensive yards and age by game week.
![Dashboard comparing  offensive yards to age and game week](/images/dashboard2.png)

## Reproducibility
Instructions for setting up your environment and running the code are provided [here](/setup.md). You can use whatever set up you prefer as long as you have installed the needed tools, adjusted environment variables, and updated files/permissions as instructed in the comments of each respective file.