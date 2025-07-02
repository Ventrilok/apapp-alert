# lambda/apapp_alert.py
import json
import boto3
import datetime
import os
import uuid
from urllib.parse import parse_qs


def lambda_handler(event, context):
    """
    Lambda function to handle tortoise distress alerts
    """
    # AWS clients
    sns = boto3.client("sns")

    # Environment variables
    topic_arn = os.environ["SNS_TOPIC_ARN"]
    project_name = os.environ.get("PROJECT_NAME", "apapp-alert")

    try:
        # Extract request data
        query_params = event.get("queryStringParameters") or {}

        # Automatic information
        timestamp = datetime.datetime.now()
        timestamp_str = timestamp.strftime("%d/%m/%Y at %H:%M:%S")
        ip_address = event["requestContext"]["identity"]["sourceIp"]
        user_agent = event["requestContext"]["identity"].get("userAgent", "Unknown")

        # Generate unique ID for this alert
        alert_id = str(uuid.uuid4())

        # Email message (detailed)
        email_message = f"""🚨 TORTOISE DISTRESS ALERT 🚨\n\n📋 ALERT DETAILS:\n⏰ Time: {timestamp_str}\n🌍 IP Address: {ip_address}\n📱 Device: {user_agent}\n🆔 Alert ID: {alert_id}\n\n⚡ Action required: Check the area quickly!\n\n---\n{project_name} automated alert system"""

        # Send detailed email
        try:
            sns.publish(
                TopicArn=topic_arn,
                Subject="🚨 Tortoise Distress Alert",
                Message=email_message,
            )
            print("Email sent successfully")
        except Exception as email_error:
            print(f"Email error: {email_error}")

        # HTML confirmation page (no geolocation, no SMS)
        html_response = f"""
        <!DOCTYPE html>
        <html lang=\"fr\">
        <head>
            <meta charset=\"UTF-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
            <title>Alerte envoyée !</title>
            <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                padding: 20px;
            }}
            .container {{
                background: rgba(255,255,255,0.15);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                max-width: 400px;
                width: 100%;
                text-align: center;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                border: 1px solid rgba(255,255,255,0.2);
            }}
            .emoji {{
                font-size: 60px;
                margin-bottom: 20px;
                display: block;
            }}
            h1 {{
                margin: 20px 0;
                font-size: 28px;
                font-weight: 600;
            }}
            p {{
                font-size: 16px;
                line-height: 1.6;
                margin-bottom: 15px;
                opacity: 0.9;
            }}
            .alert-id {{
                font-family: 'Courier New', monospace;
                background: rgba(255,255,255,0.2);
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 14px;
                margin: 20px 0;
            }}
            .time {{
                font-size: 14px;
                opacity: 0.7;
                margin-top: 30px;
            }}
            @media (max-width: 480px) {{
                .container {{ padding: 30px 20px; }}
                h1 {{ font-size: 24px; }}
                .emoji {{ font-size: 50px; }}
            }}
            </style>
        </head>
        <body>
            <div class="container">
            <span class="emoji">🐢✅</span>
            <h1>Alerte envoyée</h1>
            <p>Merci d’avoir signalé une tortue en détresse.</p>
            <p>Votre alerte a bien été envoyée.</p>
            <div class="alert-id">
                ID : {alert_id[:8]}
            </div>
            <div class="time">Envoyée le {timestamp_str}</div>
            </div>
        </body>
        </html>
        """

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
            "body": html_response,
        }

    except Exception as e:
        print(f"General error: {str(e)}")

        # Error page with fallback in case of failure
        error_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error - Apapp Alert</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                    color: white;
                    margin: 0;
                }}
                .container {{
                    background: rgba(255,255,255,0.1);
                    padding: 40px;
                    border-radius: 20px;
                    max-width: 400px;
                    margin: 0 auto;
                }}
                h1 {{ margin: 20px 0; }}
                p {{ font-size: 16px; line-height: 1.6; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ Technical Error</h1>
                <p>The alert system encountered a problem.</p>
                <p><strong>Please try again later.</strong></p>
            </div>
        </body>
        </html>
        """

        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": error_html,
        }
