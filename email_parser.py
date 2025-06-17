import imaplib
import email

# Set your credentials and email server
imap_server = 'imap.gmail.com'
email_user = 'kastum7890@gmail.com'
email_pass = 'creclldiwqrqxawy'  # Use an app password if Gmail

# Connect to the server
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(email_user, email_pass)
mail.select('inbox')

# Search and fetch the latest email
status, messages = mail.search(None, 'ALL')
email_ids = messages[0].split()
latest_email_id = email_ids[-1]
status, msg_data = mail.fetch(latest_email_id, '(RFC822)')
raw_email = msg_data[0][1]

# Parse the email
msg = email.message_from_bytes(raw_email)
print("From:", msg['From'])
print("Subject:", msg['Subject'])

# Get email body
for part in msg.walk():
    if part.get_content_type() == 'text/plain':
        print("Body:\n", part.get_payload(decode=True).decode())
