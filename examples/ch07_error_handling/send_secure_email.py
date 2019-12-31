"""
Example of sending email via SMTP and SSL/TLS.
"""

import smtplib
import ssl
from datetime import datetime as dt
from textwrap import dedent
from typing import Dict, Tuple


sender_email: str = 'pydev.bootcamp@gmail.com'
# For GMail, you'll need to enable "Allow less secure apps" in the sender's
# GMail account settings (because we're not using OAuth for sign-in)
sender_password: str = '824HZ_k2Pan7iH'
receiver_email: str = 'pydev.bootcamp@gmail.com'

# for GMail
smtp_host: str = 'smtp.gmail.com'
smtp_port: int = 587  # For gmail with starttls

time: str = dt.now().strftime('%A %b %w, %Y at %-I:%M %p')
message: str = f"""\
    Subject: Hello from Python

    This message was sent from Python at {time}."""

# Create a secure SSL context
ssl_context: ssl.SSLContext = ssl.create_default_context()

# Log in to server and send email
try:
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls(context=ssl_context)  # Secure the connection

        server.login(sender_email, sender_password)
        # Send email
        failed_recipients: Dict[str, Tuple[int, str]] = \
            server.sendmail(sender_email, receiver_email, dedent(message))

        if failed_recipients:
            print(f'failed recipients: {failed_recipients}')
except Exception as e:
    print(e)  # Print any error messages to stdout
    exit(1)
