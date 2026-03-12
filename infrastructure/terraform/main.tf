# Biomedical Data Platform — Terraform
# Example: GCP data lake foundation (adjust for AWS/Azure)

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# BigQuery dataset for analytics warehouse
resource "google_bigquery_dataset" "analytics" {
  dataset_id = "biomedical_analytics"
  location   = var.region
}

# GCS bucket for Delta Lake / Parquet
resource "google_storage_bucket" "data_lake" {
  name     = "${var.project_id}-biomedical-datalake"
  location = var.region
}

# Pub/Sub topic for FHIR ingestion
resource "google_pubsub_topic" "fhir_ingest" {
  name = "fhir-ingest"
}

variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}
