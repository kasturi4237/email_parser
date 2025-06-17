import imaplib
import email
import os
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")

imap_server = 'imap.gmail.com'
job_keywords = ['job', 'opportunity', 'interview', 'career', 'opening', 'hiring', 'application']

# Connect and login
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(email_user, email_pass)
mail.select('inbox')

# Fetch email IDs
status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()

# Create/Open output file
with open("job_emails_output.txt", "w", encoding="utf-8") as file:
    for email_id in reversed(email_ids):  # newest first
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = msg['Subject']
        sender = msg['From']
        body = ""

        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    continue
                break

        combined_text = (subject or "") + " " + body
        if any(keyword.lower() in combined_text.lower() for keyword in job_keywords):
            # Print to console
            print("From:", sender)
            print("Subject:", subject)
            print("Body:\n", body)
            print("=" * 80)

            # Write to file
            file.write(f"From: {sender}\n")
            file.write(f"Subject: {subject}\n")
            file.write("Body:\n")
            file.write(body + "\n")
            file.write("=" * 80 + "\n\n")
