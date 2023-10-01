

def send_email_notification(request):
    import os
    import smtplib
    from email.message import EmailMessage
    import yaml

    with open('.env.yaml', 'r') as file:
        env_vars = yaml.load(file, Loader=yaml.FullLoader)
        print(env_vars)  # Add this line to debug

    # Extract the request content
    data = request.get_json()

    # Set the environment variables
    for key, value in env_vars.items():
        os.environ[key] = value

    recipient_email = data.get('recipient')
    if not recipient_email:
        print("Error: Email not provided")
        return

    # Email configuration
    SENDER_EMAIL_ADDRESS = os.environ.get('SENDER_EMAIL_ADDRESS')
    SENDER_EMAIL_PASSWORD = os.environ.get('SENDER_EMAIL_PASSWORD')

    subject = data.get('subject')
    content = data.get('content')

    # Create the email message
    msg = EmailMessage()
    msg['From'] = SENDER_EMAIL_ADDRESS
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(content)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()  # Start TLS for security
            smtp.login(SENDER_EMAIL_ADDRESS, SENDER_EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("Success: Email sent successfully")
    except Exception as e:
        print(f"Error: {str(e)}")
