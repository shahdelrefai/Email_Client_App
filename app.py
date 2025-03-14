import tkinter as tk
from tkinter import messagebox
import email.mime.multipart
import requests
import smtplib

user_email = ''
user_password = ''


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
tk.Button(login_frame, text="Login", command=show_inbox).pack()
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
tk.Button(compose_frame, text="Send", command=show_inbox).pack()

root.mainloop()