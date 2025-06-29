# 🐢 Apapp Alert System

A serverless tortoise distress alert system built with Infrastructure as Code (IaC) using Terraform and AWS.

[![Terraform](https://img.shields.io/badge/Terraform-1.6.0-purple?logo=terraform)](https://terraform.io)
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20API%20Gateway%20%7C%20SNS-orange?logo=amazon-aws)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Overview

This project deploys a simple, cost-effective alert system for reporting tortoises in distress. Users scan a QR code, triggering an API Gateway endpoint that invokes a Lambda function. The Lambda sends instant SMS and email notifications to the alert recipient.

## Features

- 📱 **QR Code Integration** – One-scan alert system
- ⚡ **Instant Notifications** – SMS + Email alerts via AWS SNS
- 🌐 **Web Interface** – User-friendly confirmation page
- 🔒 **Secure & Private** – No phone number exposure
- 💰 **Low Cost** – Minimal AWS usage
- 🚀 **CI/CD Ready** – Automated deployment with GitHub Actions

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   QR Code   │───▶│ API Gateway  │───▶│   Lambda    │───▶│     SNS     │
│   Scanner   │    │   Endpoint   │    │  Function   │    │ SMS + Email │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
```

### AWS Services Used

- **Lambda** – Alert processing and HTML generation
- **API Gateway** – REST endpoint for QR codes
- **SNS** – SMS and email notifications
- **CloudWatch** – Monitoring and logs
- **S3** – Terraform state storage

## Project Structure

```
apapp-alert/
├── main.tf              # Main Terraform configuration
├── variables.tf         # Input variables
├── outputs.tf           # Output values
├── versions.tf          # Provider versions
├── README.md            # This documentation
│
├── lambda/
│   └── apapp_alert.py   # Python Lambda handler
│
└── .github/
    └── workflows/       # GitHub Actions workflows
```

## Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- GitHub Account
- Terraform 1.6.0+ (optional – runs in GitHub Actions)
- AWS CLI configured (for local development)

### 1. Repository Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/apapp-alert-terraform.git
cd apapp-alert-terraform
```

### 2. AWS Infrastructure Setup

```bash
# Create S3 bucket for Terraform state (replace with unique name)
aws s3 mb s3://apapp-alert-terraform-state-$(date +%s)
```

Update the bucket name in `versions.tf` if needed.

### 3. Configuration

Create `terraform.tfvars` with your settings:

```hcl
phone_number  = "+41123456789"        # Your phone for SMS alerts
email_address = "alert@example.com"   # Your email for detailed alerts
aws_region    = "eu-west-1"           # AWS region
project_name  = "apapp-alert"         # Project identifier
environment   = "prod"                # Environment name
```

### 4. GitHub Secrets

Configure these secrets in your GitHub repository settings:

| Secret Name             | Description         |
|------------------------|---------------------|
| `AWS_ACCESS_KEY_ID`    | AWS Access Key      |
| `AWS_SECRET_ACCESS_KEY`| AWS Secret Key      |
| `PHONE_NUMBER`         | Your phone number   |
| `EMAIL_ADDRESS`        | Your email address  |

### 5. Deploy

```bash
# Push to main branch to trigger deployment
git add .
git commit -m "Initial deployment"
git push origin main
```

GitHub Actions will automatically:

1. Validate Terraform configuration
2. Deploy infrastructure to AWS
3. Output the QR code URL

## Usage

### After Deployment

1. **Get the QR Code URL** from GitHub Actions output or Terraform output.
2. **Generate QR Codes** using any QR code generator (e.g. [QR Code Generator](https://www.qr-code-generator.com/)).
3. **Create Signage** with the QR code and instructions for users.

When a user scans the QR code, an alert is sent instantly by SMS and email to the configured recipients. The user sees a confirmation page.

## Notes

- Only AWS Lambda, API Gateway, SNS, CloudWatch, and S3 are required.
- For cost control, review your AWS usage and SNS pricing.

---

MIT License
