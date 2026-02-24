# ============================================================
# variables.tf - Input Variables
# ============================================================

variable "aws_region" {
  description = "AWS region to deploy resources into"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type (t3.micro is free tier eligible)"
  type        = string
  default     = "t3.micro"
}

variable "key_pair_name" {
  description = "Name for the AWS Key Pair resource"
  type        = string
  default     = "analytics-dashboard-key"
}

variable "public_key_path" {
  description = "Path to your SSH public key file on your local machine"
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "docker_image" {
  description = "Docker Hub image to deploy (username/repo:tag)"
  type        = string
  default     = "fredipolodev/business-analytics-dashboard:latest"
}
