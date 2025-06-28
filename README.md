# 🐢 Apapp Alert System

A serverless tortoise distress alert system built with Infrastructure as Code (IaC) using Terraform and AWS.

[![Terraform](https://img.shields.io/badge/Terraform-1.6.0-purple?logo=terraform)](https://terraform.io)
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20API%20Gateway%20%7C%20SNS-orange?logo=amazon-aws)](https://aws.amazon.com)
[![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Overview

This project deploys a complete alert system that allows people to scan QR codes and instantly send distress alerts when they find tortoises in trouble. The system provides immediate feedback to users and sends SMS/email notifications to the alert recipient.

### ✨ Features

- 📱 **QR Code Integration** - One-scan alert system
- ⚡ **Instant Notifications** - SMS + Email alerts
- 🌐 **Web Interface** - Beautiful confirmation pages
- 📍 **Geolocation Support** - Automatic location detection
- 🔒 **Secure & Private** - No phone number exposure
- 💰 **Cost Effective** - ~€1/month running costs
- 🚀 **CI/CD Ready** - Automated deployment with GitHub Actions
- 📊 **Logging & Monitoring** - Full audit trail with DynamoDB

## 🏗️ Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   QR Code   │───▶│ API Gateway  │───▶│   Lambda    │───▶│     SNS     │
│   Scanner   │    │   Endpoint   │    │  Function   │    │ SMS + Email │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │  DynamoDB   │
                                       │   Logging   │
                                       └─────────────┘
```

### AWS Services Used

- **Lambda** - Alert processing and HTML generation
- **API Gateway** - REST endpoint for QR codes
- **SNS** - SMS and email notifications
- **DynamoDB** - Alert logging and anti-spam
- **CloudWatch** - Monitoring and logs
- **S3** - Terraform state storage

## 📁 Project Structure

```
apapp-alert/
├── 📄 main.tf                        # Main Terraform configuration
├── 📄 variables.tf                   # Input variables
├── 📄 outputs.tf                     # Output values
├── 📄 versions.tf                    # Provider versions
├── 📄 terraform.tfvars               # Your private variables (create this)
├── 📄 .gitignore                     # Git ignore rules
├── 📄 README.md                      # This documentation
│
├── 📂 lambda/                        # Lambda function code
│   └── 📄 apapp_alert.py            # Python handler with embedded HTML
│
└── 📂 .github/                       # GitHub Actions workflows
    └── 📂 workflows/
        ├── 📄 terraform-plan.yml    # PR validation workflow
        ├── 📄 terraform-apply.yml   # Deployment workflow
        └── 📄 terraform-destroy.yml # Cleanup workflow
```

## 🚀 Quick Start

### Prerequisites

- AWS Account with appropriate permissions
- GitHub Account
- Terraform 1.6.0+ (optional - runs in GitHub Actions)
- AWS CLI configured (for local development)

### 1. Repository Setup

```bash
# Clone or create the repository
git clone https://github.com/yourusername/apapp-alert-terraform.git
cd apapp-alert-terraform

# Or create new repository
gh repo create apapp-alert-terraform --public
cd apapp-alert-terraform
```

### 2. AWS Infrastructure Setup

```bash
# Create S3 bucket for Terraform state (replace with unique name)
aws s3 mb s3://apapp-alert-terraform-state-$(date +%s)

# Update the bucket name in versions.tf
# backend "s3" {
#   bucket = "your-unique-bucket-name"
#   key    = "prod/terraform.tfstate"
#   region = "eu-west-1"
# }
```

### 3. Configuration

Create `terraform.tfvars` with your settings:

```hcl
# terraform.tfvars
phone_number  = "+33123456789"        # Your phone for SMS alerts
email_address = "alert@example.com"   # Your email for detailed alerts
aws_region    = "eu-west-1"          # AWS region
project_name  = "apapp-alert"        # Project identifier
environment   = "prod"               # Environment name
```

### 4. GitHub Secrets

Configure these secrets in your GitHub repository settings:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | AWS Access Key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS Secret Key | `wJalr...` |
| `PHONE_NUMBER` | Your phone number | `+33123456789` |
| `EMAIL_ADDRESS` | Your email address | `alert@example.com` |

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

## 📱 Usage

### After Deployment

1. **Get the QR Code URL** from GitHub Actions output or Terraform output:

   ```
   https://abc123.execute-api.eu-west-1.amazonaws.com/prod/alert
   ```

2. **Generate QR Codes** using any QR code generator:
   - [QR Code Generator](https://www.qr-code-generator.com/)
   - [QRCode Monkey](https://www.qrcode-monkey.com/)

3. **Create Signage** with the QR code and text like:

   ```
   🐢 TORTOISE IN DISTRESS?
   Scan this code to alert instantly
   [QR CODE HERE]
   Thank you for your help!
   ```

4. **Install Signs** in areas where tortoises might need help

### User Experience

1. **User scans QR code** with smartphone
2. **Browser opens automatically** with the alert URL
3. **Page loads and processes alert** (sends SMS + email to you)
4. **User sees confirmation page** with alert ID and timestamp
5. **You receive notifications** via SMS and email with location details

## 🛠️ Customization

### Environment Variables

The Lambda function uses these environment variables (automatically set by Terraform):

- `SNS_TOPIC_ARN` - Email notification topic
- `PHONE_NUMBER` - SMS destination number  
- `PROJECT_NAME` - Project identifier

### Terraform Variables

You can customize the deployment by modifying `terraform.tfvars`:

```hcl
aws_region     = "eu-west-1"          # Change AWS region
project_name   = "apapp-alert"        # Change project name
environment    = "prod"               # Change environment
phone_number   = "+33123456789"       # Your phone number
email_address  = "alert@example.com"  # Your email
```

### Lambda Function

To modify the alert logic or HTML pages, edit `lambda/apapp_alert.py`. The function includes:

- Alert processing logic
- SMS message formatting
- Email message formatting
- HTML success page (embedded)
- HTML error page (embedded)
- Geolocation handling
- DynamoDB logging

## 🔄 CI/CD Workflows

### Pull Request Workflow (`terraform-plan.yml`)

Triggered on PRs affecting Terraform or Lambda code:

- Validates Terraform syntax
- Runs `terraform plan`
- Posts plan results as PR comment

### Deployment Workflow (`terraform-apply.yml`)

Triggered on pushes to main branch:

- Applies infrastructure changes
- Outputs deployment results
- Updates Lambda function code

### Destroy Workflow (`terraform-destroy.yml`)

Manual workflow for cleanup:

- Destroys all AWS resources
- Requires manual confirmation
- Useful for testing or decommissioning

## 💰 Cost Estimation

| Service | Usage | Monthly Cost (EUR) |
|---------|-------|-------------------|
| Lambda | 100 invocations | ~€0.01 |
| API Gateway | 100 requests | ~€0.30 |
| SNS SMS | 10 SMS messages | ~€0.60 |
| SNS Email | Unlimited emails | Free |
| DynamoDB | On-demand, low usage | ~€0.10 |
| **Total** | | **~€1.01/month** |

*Costs may vary by region and usage patterns*

## 🔒 Security

### Best Practices Implemented

- **Least Privilege IAM** - Lambda has minimal required permissions
- **No Secrets in Code** - All sensitive data in environment variables
- **HTTPS Only** - All communications encrypted
- **Input Validation** - Proper handling of user inputs
- **Error Handling** - No sensitive information in error messages

### GitHub Security

- Branch protection rules recommended
- Secrets properly configured
- Workflows use official actions
- No sensitive data in repository

## 🐛 Troubleshooting

### Common Issues

#### Lambda Function Fails

```bash
# Check CloudWatch logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/apapp-alert"

# View recent logs
aws logs describe-log-streams --log-group-name "/aws/lambda/apapp-alert-handler"
```

#### SMS Not Received

- Verify phone number format (+33...)
- Check AWS SNS sandbox mode in your region
- Ensure SMS is supported in your AWS region

#### Email Not Received

- Check spam folder
- Verify SNS subscription confirmation
- Check SNS topic subscription status

#### Terraform State Issues

```bash
# If state is locked
terraform force-unlock LOCK_ID

# If state is corrupted
terraform refresh
```

### Monitoring

```bash
# Check API Gateway metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiName,Value=apapp-alert-api \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum

# Check Lambda errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=apapp-alert-handler \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## 🧪 Testing

### Local Testing

```bash
# Validate Terraform
terraform init
terraform validate
terraform plan

# Test Lambda function locally (requires AWS CLI)
aws lambda invoke \
  --function-name apapp-alert-handler \
  --payload '{"requestContext":{"identity":{"sourceIp":"127.0.0.1"}}}' \
  response.json
```

### End-to-End Testing

1. Deploy the system
2. Generate a test QR code with the output URL
3. Scan with your phone
4. Verify you receive SMS and email
5. Check the confirmation page displays correctly

## 🔄 Maintenance

### Regular Tasks

- **Monthly** - Review AWS costs and usage
- **Quarterly** - Update Terraform providers
- **Yearly** - Rotate AWS access keys

### Updates

```bash
# Update Terraform providers
terraform init -upgrade

# Deploy updates
git add .
git commit -m "Update infrastructure"
git push origin main
```

## 📖 Learning Resources

This project is excellent for learning:

- **Terraform** - Infrastructure as Code fundamentals
- **AWS Lambda** - Serverless function development
- **API Gateway** - REST API creation and management
- **SNS** - Notification services
- **GitHub Actions** - CI/CD pipeline creation
- **Python** - Serverless application development

### Recommended Learning Path

1. **Start with** - Basic Terraform concepts
2. **Then learn** - AWS Lambda fundamentals  
3. **Understand** - API Gateway integration
4. **Explore** - SNS notification patterns
5. **Master** - CI/CD with GitHub Actions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines

- Follow Terraform best practices
- Include tests for new features
- Update documentation
- Ensure CI/CD passes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For issues with this project:

1. Check the troubleshooting section
2. Review GitHub Actions logs
3. Check AWS CloudWatch logs
4. Create an issue in this repository

## 🙏 Acknowledgments

- Built with Terraform and AWS
- Inspired by wildlife conservation efforts
- Designed for ease of use and reliability

---

**Happy turtle helping! 🐢💚**

*Made with ❤️ for wildlife conservation*
