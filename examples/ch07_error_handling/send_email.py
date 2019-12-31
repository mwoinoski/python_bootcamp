"""
Example of sending email via SMTP.

Before running this script, launch a debug SMTP server:
    python -m smtpd -c DebuggingServer -n localhost:1025
"""

import smtplib
from datetime import datetime as dt
from textwrap import dedent
from typing import Optional, Dict, Tuple


sender_email: str = 'pydev.bootcamp@gmail.com'
receiver_email: str = 'pydev.bootcamp@gmail.com'

smtp_host_debug: str = 'localhost'
smtp_port_debug: int = 1025

time: str = dt.now().strftime('%A %b %w, %Y at %-I:%-M %p')
message: str = f"""\
    Subject: Hello from Python
    
    This message was sent from Python at {time}."""

# Log in to server and send emails
server: Optional[smtplib.SMTP] = None
failed_recipients: Dict[str, Tuple[int, str]] = {}
try:
    server: smtplib.SMTP = smtplib.SMTP(smtp_host_debug,
                                        smtp_port_debug)

    # Send email
    failed_recipients = server.sendmail(
        sender_email, receiver_email, dedent(message))

    # if sendmail() returns a Dict with items for each failed recipient.
    # An item's key is the recipient, and the value is tuple of the
    # SMTP error code and SMTP error message.
    if failed_recipients:
        print(f'failed recipients: {failed_recipients}')

except Exception as e:
    print(e)  # Print any error messages to stdout
    exit(1)

finally:
    if server:
        server.quit()

# smtplib.SMTP is a context manager, so you don't need to handle exceptions,
# you can simplify the code by omitting the try-except-finally:
#     with smtplib.SMTP(smtp_host_debug, smtp_port_debug) as server:
#         failed_recipients = server.sendmail(
#             sender_email, receiver_email, dedent(message))
#         if failed_recipients:
#             print(f'failed recipients: {failed_recipients}')
# The SMTP server connection is automatically closed at the end of the `with`
# block, even if an exception occurs
