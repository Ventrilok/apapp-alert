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
    sns = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb')
    
    # Environment variables
    topic_arn = os.environ['SNS_TOPIC_ARN']
    phone_number = os.environ['PHONE_NUMBER']
    project_name = os.environ.get('PROJECT_NAME', 'apapp-alert')
    
    try:
        # Extract request data
        query_params = event.get('queryStringParameters') or {}
        
        # Automatic information
        timestamp = datetime.datetime.now()
        timestamp_str = timestamp.strftime("%d/%m/%Y at %H:%M:%S")
        ip_address = event['requestContext']['identity']['sourceIp']
        user_agent = event['requestContext']['identity'].get('userAgent', 'Unknown')
        
        # Geolocation (if provided by browser)
        lat = query_params.get('lat', 'Not available')
        lng = query_params.get('lng', 'Not available')
        
        # Generate unique ID for this alert
        alert_id = str(uuid.uuid4())
        
        # Build alert message
        location_text = f"📍 Lat: {lat}, Lng: {lng}" if lat != 'Not available' else "📍 Location not available"
        
        # SMS message (short)
        sms_message = f"""🚨 TORTOISE IN DISTRESS
⏰ {timestamp_str}
{location_text}
🆔 {alert_id[:8]}"""
        
        # Email message (detailed)
        email_message = f"""🚨 TORTOISE DISTRESS ALERT 🚨

📋 ALERT DETAILS:
⏰ Time: {timestamp_str}
📍 Location: 
   - Latitude: {lat}
   - Longitude: {lng}
🌍 IP Address: {ip_address}
📱 Device: {user_agent}
🆔 Alert ID: {alert_id}

🔗 If geolocation available:
   Google Maps: https://maps.google.com/?q={lat},{lng}

⚡ Action required: Check the area quickly!

---
{project_name} automated alert system"""

        # Log to DynamoDB
        try:
            table = dynamodb.Table(f'{project_name}-logs')
            table.put_item(
                Item={
                    'alert_id': alert_id,
                    'timestamp': timestamp.isoformat(),
                    'ip_address': ip_address,
                    'latitude': lat,
                    'longitude': lng,
                    'user_agent': user_agent,
                    'processed': True
                }
            )
        except Exception as log_error:
            print(f"DynamoDB logging error: {log_error}")
            # Continue even if logging fails
        
        # Send SMS
        try:
            sns.publish(
                PhoneNumber=phone_number,
                Message=sms_message,
                MessageAttributes={
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': 'ApappAlert'
                    }
                }
            )
            print("SMS sent successfully")
        except Exception as sms_error:
            print(f"SMS error: {sms_error}")
        
        # Send detailed email
        try:
            sns.publish(
                TopicArn=topic_arn,
                Subject='🚨 Tortoise Distress Alert',
                Message=email_message
            )
            print("Email sent successfully")
        except Exception as email_error:
            print(f"Email error: {email_error}")
        
        # HTML confirmation page
        html_response = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Alert Sent!</title>
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
                
                .location {{
                    font-size: 12px;
                    opacity: 0.6;
                    margin-top: 10px;
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
                <h1>Alert Sent!</h1>
                <p>Thank you for reporting a tortoise in distress.</p>
                <p>The alert has been sent instantly via SMS and email.</p>
                
                <div class="alert-id">
                    ID: {alert_id[:8]}
                </div>
                
                <div class="time">Sent on {timestamp_str}</div>
                <div class="location">{location_text}</div>
            </div>
            
            <script>
                // Attempt geolocation to improve accuracy
                if ("geolocation" in navigator && "{lat}" === "Not available") {{
                    navigator.geolocation.getCurrentPosition(
                        function(position) {{
                            // Send coordinates back for more precise alert
                            fetch(window.location.href + 
                                  `?lat=${{position.coords.latitude}}&lng=${{position.coords.longitude}}&accuracy=${{position.coords.accuracy}}`
                            ).catch(err => console.log('Geolocation update failed:', err));
                        }},
                        function(error) {{
                            console.log('Geolocation denied or failed:', error);
                        }},
                        {{
                            enableHighAccuracy: true,
                            timeout: 10000,
                            maximumAge: 300000
                        }}
                    );
                }}
            </script>
        </body>
        </html>
        """
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            'body': html_response
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
                .phone {{ 
                    font-size: 24px; 
                    font-weight: bold; 
                    margin: 20px 0;
                    padding: 15px;
                    background: rgba(255,255,255,0.2);
                    border-radius: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>❌ Technical Error</h1>
                <p>The alert system encountered a problem.</p>
                <p><strong>Please contact directly:</strong></p>
                <div class="phone">{phone_number}</div>
                <p>Describe the situation and location of the tortoise in distress.</p>
            </div>
        </body>
        </html>
        """
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/html; charset=utf-8'
            },
            'body': error_html
        }