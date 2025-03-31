terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.14.1"
    }
  }
}

provider "google" {
  #   credentials = file(var.credentials)
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "zoomcamp-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class
  
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "zoomcamp-dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

resource "google_dataproc_cluster" "zoomcamp-cluster" {
  name   = var.dataproc_cluster
  region = var.region
}