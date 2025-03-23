variable "application_key" {
  description = "OVH API Application Key"
  type        = string
  sensitive   = true
}

variable "application_secret" {
  description = "OVH API Application Secret"
  type        = string
  sensitive   = true
}

variable "consumer_key" {
  description = "OVH API Consumer Key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "OVH Cloud region"
  type        = string
  default     = "GRA7"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.27"
}

variable "node_flavor" {
  description = "Node flavor/size"
  type        = string
  default     = "b2-7"  # 8 vCores, 32GB RAM
}

variable "initial_node_count" {
  description = "Initial number of nodes"
  type        = number
  default     = 3
}

variable "min_nodes" {
  description = "Minimum number of nodes"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Maximum number of nodes"
  type        = number
  default     = 10
}