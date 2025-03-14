from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(server, email_from, email_to, email_subject, email_body):
    compose_email = MIMEMultipart()

    compose_email['From'] = email_from
    compose_email['To'] = email_to
    compose_email['Subject'] = email_subject
    compose_email.attach(MIMEText(email_body, 'plain'))

    try:
        server.sendmail(email_from, email_to, compose_email.as_string())  # Send email
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return e


