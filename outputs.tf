# outputs.tf
output "api_gateway_url" {
  description = "API Gateway URL for QR codes"
  value       = "${aws_api_gateway_stage.apapp_stage.invoke_url}/alert"
}

output "sns_topic_arn" {
  description = "SNS topic ARN"
  value       = aws_sns_topic.apapp_alerts.arn
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.apapp_alert.function_name
}

output "qr_code_url" {
  description = "URL to use for QR code generation"
  value       = "${aws_api_gateway_stage.apapp_stage.invoke_url}/alert"
}
