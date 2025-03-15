from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox
from ReceiveEmail import EmailReceiver as EmailReceiver
from SendEmail import EmailSender as EmailSender


user_email = ''
user_password = ''
email_list = []

eSender: EmailSender
eReceiver: EmailReceiver


def login():
    global user_email, user_password, eSender, eReceiver
    user_email = email_entry.get()
    user_password = password_entry.get()

    if check_login_inputs_format() is False:
        return

    eSender = EmailSender(user_email, user_password)
    eReceiver = EmailReceiver(user_email, user_password)

    login_status = login_authenticate()
    if login_status is False:
        return False

    start_new_email_checking()
    show_inbox()

def login_authenticate():
    stmp_connection = eSender.login()
    imap_connection = eReceiver.login()

    if stmp_connection and imap_connection:
        show_success_messagebox("Login successful.")
        return True

    show_error_messagebox("authenticate: Check your App Password.")
    clear_inputs([password_entry])

    if stmp_connection is None and imap_connection is False:
        print("Error in both SMTP and IMAP logins.")
    if stmp_connection is None:
        print("Error in SMTP login.")
    else:
        print("Error in IMAP login.")
    return False

def check_login_inputs_format():
    check = check_inputs_format()
    if check is not True:
        show_error_messagebox(f"login: {check}")
        return False
    return True

def check_inputs_format():
    global user_email, user_password
    user_email = user_email.strip()
    user_password = user_password.strip()

    if not user_email or not user_password:
        return 'Invalid email and password.'
    if not user_email.endswith("@gmail.com"):
        return 'Invalid email.'
    if not user_password:
        return 'Invalid password.'
    return True

def send_email():
    email_to = email_to_entry.get()
    email_subject = email_subject_entry.get()
    email_body = email_body_entry.get("1.0", tk.END)

    send_status = eSender.send_email(email_to, email_subject, email_body)

    if send_status is not True:
        show_error_messagebox(f"send email: {send_status}")
        return

    show_success_messagebox("Email sent successfully!")
    show_inbox()

def fetch_emails():
    global email_list
    email_list = eReceiver.fetch_emails()
    email_list = list(reversed(email_list))

    email_display.config(state=tk.NORMAL)
    email_display.delete("1.0", tk.END)
    if email_list:
        for email_item in email_list:
            date = email_item.get('date')

            email_display.insert(tk.END, f"{email_item.get('subject')}\t\t\t\t\t\t\t\t\t\t{date}\n", "subject")
            email_display.insert(tk.END, f"From: {email_item.get('from')}\n\n", "from")
    else:
        email_display.insert(tk.END, "No emails to display.\n")

    email_display.config(state=tk.DISABLED)

def start_new_email_checking():
    """Check for new email periodically using after method."""
    received = eReceiver.fetch_new_email()
    if received:
        time.sleep(3)
        fetch_emails()
    root.after(10000, start_new_email_checking)  # Call the function again after 10 seconds


def open_email(event):
    """Open a window displaying the full email when clicked."""
    index = email_display.index(tk.CURRENT).split('.')[0]
    try:
        email_index = int(index) // 3  # Each email is 3 lines apart
        email_data = email_list[email_index]

        email_window = tk.Toplevel(root)
        email_window.title("Email Details")

        subject_label = tk.Label(email_window, text=email_data["subject"], font=title_font, wraplength=400)
        subject_label.pack(pady=(10, 5))

        from_label = tk.Label(email_window, text=f"From: {email_data['from']}", font=from_font)
        from_label.pack(pady=(0, 10))

        body_text = tk.Text(email_window, wrap="word", height=60, width=80)
        body_text.insert("1.0", email_data["body"])
        body_text.config(state="disabled")
        body_text.pack(padx=10, pady=5)
        email_window.geometry("800x1000")
    except:
        pass


def clear_inputs(inputs):
    for input in inputs:
        input.delete(0, 'end')

def show_error_messagebox(message):
    messagebox.showerror('Error', f"❌ Failed to {message}")

def show_success_messagebox(message):
    messagebox.showinfo('Success', f"✅ {message}")


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
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
#root.attributes('-fullscreen', True)

# Define fonts
title_font = ("Arial", 24, "bold")
label_font = ("Arial", 18)
entry_font = ("Arial", 20)
button_font = ("Arial", 16)
listbox_font = ("Arial", 16)
text_font = ("Arial", 18)
subject_font = ("Arial", 18, "bold")
from_font = ("Arial", 16, "italic")

# Login Frame
login_frame = tk.Frame(root)
tk.Label(login_frame, text="Email:", font=label_font).pack()
email_entry = tk.Entry(login_frame, font=entry_font, width=35)
email_entry.pack()
tk.Label(login_frame, text="Password:", font=label_font).pack()
password_entry = tk.Entry(login_frame, show="*", font=entry_font, width=35)
password_entry.pack()
tk.Button(login_frame, text="Login", font=button_font, command=login, width=10).pack(pady=10)
login_frame.pack(fill=tk.BOTH, expand=True, pady=400)

# Inbox Frame
inbox_frame = tk.Frame(root)
tk.Label(inbox_frame, text="Inbox", font=title_font).pack()
email_display = tk.Text(inbox_frame, height=20, width=90, wrap="word", font=text_font)
email_display.tag_config("subject", font=subject_font)
email_display.tag_config("from", font=from_font)
email_display.config(state=tk.DISABLED)
email_display.pack(fill=tk.BOTH, expand=True, pady=200)
email_display.bind("<Button-1>", open_email)
tk.Button(inbox_frame, text="Refresh", font=button_font, command=fetch_emails).pack()
tk.Button(inbox_frame, text="Compose", font=button_font, command=show_compose).pack()

# Compose Email Frame
compose_frame = tk.Frame(root)
tk.Label(compose_frame, text="To:", font=label_font).pack(pady=(200,0))
email_to_entry = tk.Entry(compose_frame, font=entry_font)
email_to_entry.pack()
tk.Label(compose_frame, text="Subject:", font=label_font).pack()
email_subject_entry = tk.Entry(compose_frame, font=entry_font)
email_subject_entry.pack()
tk.Label(compose_frame, text="Body:", font=label_font).pack()
email_body_entry = tk.Text(compose_frame, height=10, font=entry_font)
email_body_entry.pack()
tk.Button(compose_frame, text="Send", font=button_font, command=send_email).pack(pady=10)
tk.Button(compose_frame, text="Back", font=button_font, command=show_inbox).pack(pady=10)


root.mainloop()