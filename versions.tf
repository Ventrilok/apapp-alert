# versions.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    bucket = "apapp-alert-terraform-state"
    key    = "prod/terraform.tfstate"
    region = "eu-west-1"
    # PAS de ligne dynamodb_table !
  }
}

provider "aws" {
  region = var.aws_region
}
