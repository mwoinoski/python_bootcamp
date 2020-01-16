"""
Example of sending HTML email via SMTP and SSL/TLS.
"""

import os
import smtplib
import ssl
from datetime import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Tuple


username: str = os.environ['USER'].replace('CORP\\', '')  # Delete Amazon's junk
sender_email: str = f'{username}.python.bootcamp@gmail.com'
# For GMail, you'll need to enable "Allow less secure apps" in the sender's
# GMail account settings (because we're not using OAuth for sign-in)
sender_password: str = '824HZ_k2Pan7iH'
receiver_email: str = f'{username}@sutterhealth.org'

# for GMail
smtp_host: str = 'smtp.gmail.com'
smtp_port: int = 587  # For gmail with starttls

time: str = dt.now().strftime('%A %b %w, %Y at %-I:%M %p')

plain_message: str = f"""\
    This is a plain text message from a Python application,
    sent at {time}
    
    No formatting of any kind."""

html_message: str = f"""\
    <html>
        <body>
            <h1>Message from Python Application</h1>
            <p>This is an HTML message sent at {time}</p>
            <p>It supports the usual HTML features:</p>
            <ul>
                <li>Different heading levels</li>
                <li>Lists</li>
                <li><a href='https://en.wikipedia.org/wiki/Hyperlink'>
                    Links</a></li>
                <li>And the other features you know and love</li>
            </ul>
        </body>
    </html>"""

message: MIMEMultipart = MIMEMultipart('alternative')
message['Subject'] = 'Notification from Python app'
message['From'] = sender_email
message['To'] = receiver_email

# Turn these into plain/html MIMEText objects
plain_part: MIMEText = MIMEText(plain_message, 'plain')
html_part: MIMEText = MIMEText(html_message, 'html')

# Add HTML and plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(plain_part)
message.attach(html_part)

# Log in to server and send email
try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        ssl_context: ssl.SSLContext = ssl.create_default_context()
        server.starttls(context=ssl_context)  # Secure the connection
        server.login(sender_email, sender_password)
        failed_recipients: Dict[str, Tuple[int, str]] = server.sendmail(
            sender_email, receiver_email, message.as_string())
        if failed_recipients:
            print(f'failed recipients: {failed_recipients}')

except Exception as e:
    print(e)  # Print any error messages to stdout
    exit(1)
