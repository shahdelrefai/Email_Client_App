import email
from email.header import decode_header
import imaplib
import time

class EmailReceiver:
    def __init__(self, email_address, app_password):
        self.mail = None  # IMAP Server
        self.user_email = email_address
        self.user_app_password = app_password
        self.email_list = []

    def login(self):
        """Connect to gmail using IMAP protocol"""
        try:
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.mail.login(self.user_email, self.user_app_password)
            return True
        except Exception as e:
            print("❌ Error:", e)
            return False

    def fetch_emails(self, limit=10):
        """Fetch a list of latest (limit) emails from the inbox"""
        self.mail.select("inbox")
        status, messages = self.mail.search(None, 'ALL')
        email_ids = messages[0].split()[-limit:]

        emails = []
        for email_id in email_ids:
            email_data = self._fetch_email_by_id(email_id)
            if email_data:
                emails.append(email_data)
        return emails

    def fetch_latest_email(self):
        """Fetch the latest email"""
        return self.fetch_emails(limit=1)[0] if self.fetch_emails(limit=1) else None

    def _fetch_email_by_id(self, email_id):
        """Fetch an email by its ID"""
        status, message_data = self.mail.fetch(email_id, '(RFC822)')
        for part in message_data:
            if isinstance(part, tuple):
                message = email.message_from_bytes(part[1])
                return self._parse_email(message)
        return None

    def _parse_email(self, message):
        """Parse the email content"""
        subject, encoding = decode_header(message['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')

        email_info = {
            "subject": subject,
            "from": message.get('From'),
            "body": self._get_body(message),
            "id": message["Message-ID"]
        }
        return email_info

    def _get_body(self, message):
        """Extract the body of the email"""
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain" and "attachment" not in str(part.get('Content-Disposition')):
                    return part.get_payload(decode=True).decode()
        elif message.get_content_type() == "text/plain":
            return message.get_payload(decode=True).decode()
        return None

    def compare_and_add_email(self, latest_email_info):
        """Compare and add the latest email if it's not already in the list"""
        if latest_email_info and not self._email_exists(latest_email_info):
            self.email_list.append(latest_email_info)
            return True
        return False

    def _email_exists(self, email_info):
        """Check if an email already exists in the list"""
        return any(existing_email['id'] == email_info['id'] for existing_email in self.email_list)

    def fetch_new_email_periodically(self, interval=60):
        """Fetch the latest email every interval and compare it"""
        while True:
            latest_email_info = self.fetch_latest_email()
            if latest_email_info and self.compare_and_add_email(latest_email_info):
                print(f"New email added: {latest_email_info['subject']} from {latest_email_info['from']}")
            else:
                print("No new emails detected.")
            time.sleep(interval)



