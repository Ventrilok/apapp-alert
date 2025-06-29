# main.tf

# S3 bucket for storing Terraform state (create manually first)
# aws s3 mb s3://apapp-alert-terraform-state

# IAM Role pour Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# Policy pour permettre à Lambda d'utiliser SNS et CloudWatch
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = [
          aws_sns_topic.apapp_alerts.arn,
          "*" # Pour les SMS directs
        ]
      }
    ]
  })
}

# SNS Topic for email alerts
resource "aws_sns_topic" "apapp_alerts" {
  name = "${var.project_name}-alerts"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# SNS Subscription for email
resource "aws_sns_topic_subscription" "email_alerts" {
  topic_arn = aws_sns_topic.apapp_alerts.arn
  protocol  = "email"
  endpoint  = var.email_address
}

# Archive Lambda code
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/apapp_alert.py"
  output_path = "${path.module}/lambda/apapp_alert.zip"
}

# Lambda Function
resource "aws_lambda_function" "apapp_alert" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "${var.project_name}-handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "apapp_alert.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30
  memory_size   = 128

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      SNS_TOPIC_ARN = aws_sns_topic.apapp_alerts.arn
      PHONE_NUMBER  = var.phone_number
      PROJECT_NAME  = var.project_name
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.apapp_alert.function_name}"
  retention_in_days = 14

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# API Gateway REST API
resource "aws_api_gateway_rest_api" "apapp_api" {
  name        = "${var.project_name}-api"
  description = "API for apapp alert system"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

# API Gateway resource for /alert
resource "aws_api_gateway_resource" "alert_resource" {
  rest_api_id = aws_api_gateway_rest_api.apapp_api.id
  parent_id   = aws_api_gateway_rest_api.apapp_api.root_resource_id
  path_part   = "alert"
}

# GET method for /alert
resource "aws_api_gateway_method" "alert_get" {
  rest_api_id   = aws_api_gateway_rest_api.apapp_api.id
  resource_id   = aws_api_gateway_resource.alert_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

# Lambda integration
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.apapp_api.id
  resource_id = aws_api_gateway_resource.alert_resource.id
  http_method = aws_api_gateway_method.alert_get.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.apapp_alert.invoke_arn
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "api_gateway_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.apapp_alert.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.apapp_api.execution_arn}/*/*"
}

# API Gateway deployment
resource "aws_api_gateway_deployment" "apapp_deployment" {
  depends_on = [
    aws_api_gateway_method.alert_get,
    aws_api_gateway_integration.lambda_integration,
  ]

  rest_api_id = aws_api_gateway_rest_api.apapp_api.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.alert_resource.id,
      aws_api_gateway_method.alert_get.id,
      aws_api_gateway_integration.lambda_integration.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

# API Gateway stage
resource "aws_api_gateway_stage" "apapp_stage" {
  deployment_id = aws_api_gateway_deployment.apapp_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.apapp_api.id
  stage_name    = "api"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
