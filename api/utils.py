import smtplib
from email.mime.text import MIMEText

from decouple import config

# Read environment variables from the .env file
SMTP_SERVER = config('SMTP_SERVER') 
SMTP_PORT = config('SMTP_PORT', default=587, cast=int)
SMTP_USERNAME = config('SMTP_USERNAME')
SMTP_PASSWORD = config('SMTP_PASSWORD')
SENDER_EMAIL = config('SENDER_EMAIL')



def populate_email_template(email_template, employee):
    # Retrieve the template content
    template_content = email_template.template_content
    
    # Replace placeholders with actual content
    template_content = template_content.replace('{{employee_name}}', employee.name)
    template_content = template_content.replace('{{event_type}}', email_template.event_type)
    # Add more replacements as needed for other placeholders
    
    return template_content


def send_email(recipient_email, email_content):
    # Email configuration
    smtp_server = SMTP_SERVER
    smtp_port = 587
    smtp_username = SMTP_USERNAME
    smtp_password = SMTP_PASSWORD
    sender_email = SENDER_EMAIL

    # Create the email message
    msg = MIMEText(email_content, 'html')
    msg['Subject'] = 'Event Notification'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, [recipient_email], msg.as_string())
        print('Email sent successfully')
    except Exception as e:
        print(f'Email sending failed: {str(e)}')
