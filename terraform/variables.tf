# Uncomment code and add credentials if you did not authenticate
# using gcloud shell commands.
#
# variable "credentials" {
#   description = "My Credentials"
#   default     = "./keys/my-creds.json"
# }

variable "project" {
  description = "Project"
  default     = "dtc-de-zoomcamp-446201" # replace with your project
}

variable "location" {
  description = "Project Location"
  default     = "US" # replace with your project location
}

variable "region" {
  description = "Project Region"
  default     = "us-central1" # replace with your project region
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "zoomcamp"
}

variable "gcs_bucket_name" {
  description = "Storage Bucket Name"
  default     = "zoomcamp-446201-bucket" # replace with your bucket name
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "dataproc_cluster" {
  description = "Dataproc Cluster Name"
  default = "nfl-zoomcamp-cluster"
}