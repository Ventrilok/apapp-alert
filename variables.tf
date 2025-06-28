variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "phone_number" {
  description = "Phone number for SMS alerts"
  type        = string
  sensitive   = true
}

variable "email_address" {
  description = "Email address for alerts"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "apapp-alert"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}
