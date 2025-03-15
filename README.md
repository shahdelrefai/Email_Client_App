# Shahd's Email Client Application Documentation

## Overview
This GUI python application is for sending and receiving emails. The project consists of three main files:

```
project-folder/
├── SendEmail.py                 # Handles sending emails via SMTP protocol
├── ReceiveEmail.py              # Handles receiving emails via IMAP protocol
└── app.py                       # Serves as the main entry point to the application, integrating the sending and receiving functionalities
```

## Features
- Interactive GUI interface.
- Login.
- Receive and read emails from an inbox.
- Error Handling.

## Installation

### Prerequisites
Ensure you have Python installed (preferably Python 3.x). You can check your Python version by running:
```bash
python --version
```

### Clone the Repository
```bash
git clone https://github.com/shahdelrefai/Email_Client_App.git
cd Email_Client_App
```

### Install Dependencies
This application requires Python built in libraries which are: `tkinter`, `smtplib`, `imaplib`, `email`, `os`, `time`and `datetime`, so need for installations. </br>

## Usage

### Running the Application
To start the application, run:
```bash
python app.py
```


## Dependencies
The application relies on the following libraries:
- `tkinter` (for GUI)
- `smtplib` (for sending emails)
- `imaplib` (for receiving emails)
- `email`   (for handling email content)
- `os`      (for notifications)

## Login Authentication
Make sure you use a valid gmail address along with a valid app password.

## Code Walkthrough

### ◉`EmailSender` class inside `SendEmail.py`
This class is responsible for sending emails using the `smtplib` module. The main steps include:
1. **Import necessary modules**: Imports `smtplib`, `email.mime` components, and other required libraries.
2. **Set up SMTP connection**: Connects to an SMTP server (e.g., Gmail, Outlook) using login credentials.
3. **Create the email message**: Uses `MIMEMultipart` to create the email body and attach files if needed.
4. **Send the email**: Uses `smtp.sendmail()` to send the email to the specified recipient(s).

### ◉`EmailReceiver` class inside `ReceiveEmail.py`
This script retrieves emails from an inbox using the `imaplib` module. The main steps include:
1. **Import necessary modules**: Includes `imaplib`, `email`, and related utilities for parsing messages.
2. **Connect to IMAP server**: Logs into the email account using credentials.
3. **Select inbox and search for emails**: Uses IMAP queries to find unread or specific emails.
4. **Fetch email contents**: Reads email data, extracts the subject, sender, and body.
5. **Handle attachments (if any)**: Saves and processes any email attachments.
6. **Close the connection**: Ensures the IMAP session is closed properly.

### ◉`app.py`
This script serves as the main entry point, integrating the sending and receiving functionalities. The main steps include:
1. **Import `SendEmail` and `ReceiveEmail` modules**.
2. **Provide a GUI interface**:
    - Login page.
    - Inbox page.
    - Compose email page.

## Tests
## 1. Login
### 1.1 Invalid input formats
<img width="1680" alt="Screenshot 2025-03-15 at 7 11 04 AM" src="https://github.com/user-attachments/assets/77fb2c88-3657-4e8c-a9e6-9cdfab032f02" />
<img width="1680" alt="Screenshot 2025-03-15 at 7 14 03 AM" src="https://github.com/user-attachments/assets/8e55f5f5-4286-4242-9ebc-58e2cbdf1cf6" />

### 1.2 Account authentication failure
<img width="1680" alt="Screenshot 2025-03-15 at 7 14 41 AM" src="https://github.com/user-attachments/assets/194d4033-bda1-4320-b28c-c00ade9d0e7c" />

### 1.3 Login Successful
<img width="1680" alt="Screenshot 2025-03-15 at 7 16 32 AM" src="https://github.com/user-attachments/assets/e271145e-a44b-4f25-8ce6-63a70bed1535" />

## 2. Inbox
### 2.1 Mailbox
<img width="1680" alt="Screenshot 2025-03-15 at 7 47 52 AM" src="https://github.com/user-attachments/assets/925dca06-0ddf-4ad1-b55a-580e7644bf52" />

### 2.2 Email body (when email pressed)
<img width="1680" alt="Screenshot 2025-03-15 at 7 50 28 AM" src="https://github.com/user-attachments/assets/9eee647e-b650-4265-9941-5520d61a7ddb" />

### 2.3 New Email Notification
<img width="1680" alt="Screenshot 2025-03-15 at 7 51 21 AM" src="https://github.com/user-attachments/assets/2f6f5faa-1249-483a-b585-dfee2a1e80cb" />

### 2.4 Automatic refresh after 3 seconds from receiving notification
<img width="1680" alt="Screenshot 2025-03-15 at 7 51 36 AM" src="https://github.com/user-attachments/assets/1f5341b0-d71f-4ed3-88f9-f12d27b9ab59" />


## 3. Email Compose
<img width="1680" alt="Screenshot 2025-03-15 at 7 53 26 AM" src="https://github.com/user-attachments/assets/26eb9f38-0f1d-4a6f-81f4-ab0941d7848f" />

### 3.1 Error Handling
<img width="1680" alt="Screenshot 2025-03-15 at 7 55 15 AM" src="https://github.com/user-attachments/assets/9633a708-e927-4be7-acf8-3de133be992e" />

### 3.2 Sending
<img width="1680" alt="Screenshot 2025-03-15 at 7 56 48 AM" src="https://github.com/user-attachments/assets/23b9d7b5-6fe4-4456-be26-13d232aee31d" />
<img width="1792" alt="Screenshot 2025-03-15 at 7 59 07 AM" src="https://github.com/user-attachments/assets/ed9ea143-1d7f-4541-a98c-470acb270792" />




