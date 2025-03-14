import tkinter as tk
from tkinter import messagebox
import email.mime.multipart
import requests
import smtplib

user_email = ''
user_password = ''


def login():
    global user_email, user_password
    user_email = email_entry.get()
    user_password = password_entry.get()

    if check_inputs_format() is False:
        return

    server = gmail_login_authenticate()
    if server is None:
        messagebox.showerror('Error', 'Unable to login')
        clear_inputs([email_entry])
        return

    show_inbox()


def gmail_login_authenticate():
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # Connect securely
        server.login(user_email, user_password)  # Authenticate
        print("✅ Login successful!")
        return server  # Return the logged-in server object
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed: Check your App Password.")
    except Exception as e:
        print("❌ Error:", e)

    return None


def check_inputs_format():
    check = check_format()
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


def check_format():
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

    if email_error and password_error :
        return 'both'
    elif email_error:
        return 'email'
    else:
        return 'password'


def clear_inputs(inputs):
    for input in inputs:
        input.delete(0, 'end')


# Show Inbox Page
def show_inbox():
    login_frame.pack_forget()
    compose_frame.pack_forget()
    inbox_frame.pack()


# Show Compose Email Page
def show_compose():
    inbox_frame.pack_forget()
    compose_frame.pack()


# GUI Setup
root = tk.Tk()
root.title("Mail.tm Email Client")
root.geometry("400x400")

# Login & Sign-Up Frame
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
email_list = tk.Listbox(inbox_frame, height=10)
email_list.pack()
tk.Button(inbox_frame, text="Compose", command=show_compose).pack()

# Compose Email Frame
compose_frame = tk.Frame(root)
tk.Label(compose_frame, text="To:").pack()
recipient_entry = tk.Entry(compose_frame)
recipient_entry.pack()
tk.Label(compose_frame, text="Subject:").pack()
subject_entry = tk.Entry(compose_frame)
subject_entry.pack()
tk.Label(compose_frame, text="Body:").pack()
body_entry = tk.Text(compose_frame, height=5)
body_entry.pack()
tk.Button(compose_frame, text="Send", command=show_compose).pack()

root.mainloop()