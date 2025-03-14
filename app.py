import imaplib
import tkinter as tk
from tkinter import messagebox
import smtplib
import SendEmail
import RecieveEmail

user_email = ''
user_password = ''
SMTP_server = None
IMAP_server = None

def login():
    global user_email, user_password, SMTP_server
    user_email = email_entry.get()
    user_password = password_entry.get()

    if check_login_inputs_format() is False:
        return

    login_status = login_authenticate()
    if login_status is False:
        clear_inputs([password_entry])
        return

    show_inbox()


def login_authenticate():
    global SMTP_server, IMAP_server
    SMTP_server = smtp_login_authenticate()
    IMAP_server = imap_login_authenticate()

    if SMTP_server and IMAP_server:
        messagebox.showinfo('Success', '✅ Login successful.')
        print("✅ Login successful!")
        return True

    messagebox.showerror('Error', "❌ Authentication failed: Check your App Password.")
    if SMTP_server is None and IMAP_server is None:
        print("Error in both SMTP and IMAP logins.")
    if SMTP_server is None:
        print("Error in SMTP login.")
    else:
        print("Error in IMAP login.")
    return False


def smtp_login_authenticate():
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(user_email, user_password)
        return server
    except smtplib.SMTPAuthenticationError:
        return None
    except Exception as e:
        print("❌ Error:", e)
        return None


def imap_login_authenticate():
    try:
        server = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        server.login(user_email, user_password)
        return server
    except Exception as e:
        print("❌ Error:", e)
        return None


def send_email():
    email_to = email_to_entry.get()
    email_subject = email_subject_entry.get()
    email_body = email_body_entry.get("1.0", tk.END)

    send_status = SendEmail.send_email(SMTP_server, user_email, email_to, email_subject, email_body)
    if send_status is not True:
        messagebox.showerror('Error', f"❌ Failed to send email: {send_status}")
        return

    messagebox.showinfo('Success', "✅ Email sent successfully!")
    show_inbox()


def fetch_emails():
    emails = RecieveEmail.fetch_emails(IMAP_server)

    email_listbox.delete(0, tk.END)  # Clear existing emails
    for email_item in emails:
        email_listbox.insert(tk.END, f"Subject: {email_item['subject']} | From: {email_item['from']}")


def check_login_inputs_format():
    check = login_check_format()
    match check:
        case 'both':
            messagebox.showerror('Error', 'Error in format of both email and password')
        case 'email':
            messagebox.showerror('Error', 'Error in format of email')
        case 'password':
            messagebox.showerror('Error', 'Error in format of password')
        case _:
            return True

    return False


def login_check_format():
    global user_email, user_password
    user_email = user_email.strip()
    user_password = user_password.strip()

    email_error = False
    password_error = False

    if not user_email:
        email_error = True
    if not user_password:
        password_error = True
    if not user_email.endswith("@gmail.com"):
        email_error = True

    if email_error and password_error:
        return 'both'
    return 'email' if email_error else 'password' if password_error else 'True'


def clear_inputs(inputs):
    for input in inputs:
        input.delete(0, 'end')


# Show Inbox Page
def show_inbox():
    login_frame.pack_forget()
    compose_frame.pack_forget()
    inbox_frame.pack()
    fetch_emails()


# Show Compose Email Page
def show_compose():
    inbox_frame.pack_forget()
    compose_frame.pack()


# GUI Setup
root = tk.Tk()
root.title("Shahd\'s Email Client App")
root.geometry("400x400")

# Login Frame
login_frame = tk.Frame(root)
tk.Label(login_frame, text="Email:").pack()
email_entry = tk.Entry(login_frame)
email_entry.pack()
tk.Label(login_frame, text="Password:").pack()
password_entry = tk.Entry(login_frame, show="*")
password_entry.pack()
tk.Button(login_frame, text="Login", command=login).pack()
login_frame.pack()

# Inbox Frame
inbox_frame = tk.Frame(root)
tk.Label(inbox_frame, text="Inbox", font=("Arial", 14)).pack()
email_listbox = tk.Listbox(inbox_frame, height=10, width=50)
email_listbox.pack()
tk.Button(inbox_frame, text="Refresh", command=fetch_emails).pack()
tk.Button(inbox_frame, text="Compose", command=show_compose).pack()

# Compose Email Frame
compose_frame = tk.Frame(root)
tk.Label(compose_frame, text="To:").pack()
email_to_entry = tk.Entry(compose_frame)
email_to_entry.pack()
tk.Label(compose_frame, text="Subject:").pack()
email_subject_entry = tk.Entry(compose_frame)
email_subject_entry.pack()
tk.Label(compose_frame, text="Body:").pack()
email_body_entry = tk.Text(compose_frame, height=5)
email_body_entry.pack()
tk.Button(compose_frame, text="Send", command=send_email).pack()

root.mainloop()