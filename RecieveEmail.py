import email
from email.header import decode_header
import imaplib


def fetch_emails(mail):
    mail.select("inbox")

    status, messages = mail.search(None, 'ALL')

    email_ids = messages[0].split()[-10:]
    email_list = []

    for email_id in email_ids:
        status, message_data = mail.fetch(email_id, '(RFC822)')
        for part in message_data:
            if isinstance(part, tuple):
                message = email.message_from_bytes(part[1])
                subject, encoding = decode_header(message['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')
                from_ = message.get('From')

                email_info = {
                    "subject": subject,
                    "from": from_,
                    "body": get_body(message)
                }
                email_list.append(email_info)

    return email_list


def get_body(message):
    if message.is_multipart():
        for part in message.walk():
            content_type, content = get_part_content(part)
            if "attachment" not in content:
                if content_type == "text/plain":
                    return decode_body(part)
    else:
        content_type = message.get_content_type()
        if content_type == "text/plain":
            return decode_body(message)

    return None


def get_part_content(part):
    return part.get_content_type(), str(part.get('Content-Disposition'))


def decode_body(message):
    return message.get_payload(decode=True).decode()