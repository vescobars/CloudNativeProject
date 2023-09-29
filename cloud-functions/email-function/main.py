import os
import smtplib
from email.message import EmailMessage
from flask import jsonify, request
from datetime import datetime


def send_email_notification(request):
    # Extract data from the request
    data = request.get_json()
    recipient_email = data.get("email")
    if not recipient_email:
        return jsonify({"error": "Email not provided"}), 400

    # Email configuration
    SENDER_EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    SENDER_EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD ')
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
            smtp.login(SENDER_EMAIL_ADDRESS, SENDER_EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Success")
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
