import os
import smtplib
from email.message import EmailMessage
import yaml
import requests

def send_email_notification(request):
    tzinfo = timezone(timedelta(hours=-5.0))
    with open('.env.yaml', 'r') as file:
        env_vars = yaml.load(file, Loader=yaml.FullLoader)
        print(env_vars)  # Add this line to debug

    # Set the environment variables
    for key, value in env_vars.items():
        os.environ[key] = value

    recipient_email = request.get("recipient")
    if not recipient_email:
        print("Error: Email not provided")
        return

    # Email configuration
    SENDER_EMAIL_ADDRESS = os.environ.get('SENDER_EMAIL_ADDRESS')
    SENDER_EMAIL_PASSWORD = os.environ.get('SENDER_EMAIL_PASSWORD')
    SUBJECT = "Credit Card Processing Confirmation"
    CONTENT = "Your credit card has been processed completely without any issues."

    # Create the email message
    msg = EmailMessage()
    msg['From'] = SENDER_EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = SUBJECT
    msg.set_content(CONTENT)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Start TLS for security
            smtp.login(SENDER_EMAIL_ADDRESS, SENDER_EMAIL_PASSWORD)
            smtp.send_message(msg)

        print(f"Success: Email sent successfully at Current time EST: {datetime.now(tzinfo)} to {recipient_email}")
    except Exception as e:
        print(f"Error: {str(e)}")

