terraform {
  required_providers {
    ovh = {
      source  = "ovh/ovh"
      version = "~> 0.40.0"
    }
  }
}

provider "ovh" {
  endpoint           = "ovh-eu"
  application_key    = var.application_key
  application_secret = var.application_secret
  consumer_key       = var.consumer_key
}

resource "ovh_cloud_project_kube" "modumind_cluster" {
  name         = "modumind-cluster"
  region       = var.region
  version      = var.kubernetes_version
}

resource "ovh_cloud_project_kube_nodepool" "main_pool" {
  kube_id       = ovh_cloud_project_kube.modumind_cluster.id
  name          = "main-pool"
  flavor_name   = var.node_flavor
  desired_nodes = var.initial_node_count
  min_nodes     = var.min_nodes
  max_nodes     = var.max_nodes
  autoscale     = true
}