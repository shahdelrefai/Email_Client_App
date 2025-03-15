from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class EmailSender:
    def __init__(self, email_address, app_password):
        self.mail = None
        self.user_email = email_address
        self.user_app_password = app_password

    def login(self):
        """Connect to gmail using STMP protocol"""
        try:
            self.mail = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            self.mail.login(self.user_email, self.user_app_password)
            return True
        except Exception as e:
            print("❌ Error:", e)
            return False

    def send_email(self, email_to, email_subject, email_body):
        compose_email = MIMEMultipart()

        compose_email['From'] = self.user_email
        compose_email['To'] = email_to
        compose_email['Subject'] = email_subject
        compose_email.attach(MIMEText(email_body, 'plain'))

        try:
            self.mail.sendmail(self.user_email, email_to, compose_email.as_string())  # Send email
            print("✅ Email sent successfully!")
            return True
        except Exception as e:
            print("❌ Failed to send email:", e)
            return e