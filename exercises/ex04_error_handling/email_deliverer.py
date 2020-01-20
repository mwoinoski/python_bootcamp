"""
Example of sending HTML email via SMTP and SSL/TLS.
"""

import os
import smtplib
import ssl
from datetime import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Tuple, ClassVar

# TODO: import logging.config


class EmailDeliverer:
    """ EmailDeliverer defines methods for sending emailto an SMTP host """
    smtp_host: str
    smtp_port: int

    # TODO: initialize a logging.Logger instance

    def __init__(self, smtp_host: str, smtp_port: int) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        # TODO: Initialize the Logger.
        #       For the logger's name, use self.logger_name

        # TODO: assign the logger to self.logger


    def send(self, sender_addr: str, sender_password: str, to_addr: str,
             subject: str, plain_message: str, html_message: str):

        # TODO: write a debug message with the value of some of the arguments
        #       to this function


        # TODO: write a info message with the recipients address


        message: MIMEMultipart = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender_addr
        message['To'] = to_addr

        # Turn these into plain/html MIMEText objects
        plain_part: MIMEText = MIMEText(plain_message, 'plain')
        html_part: MIMEText = MIMEText(html_message, 'html')

        # Add HTML and plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(plain_part)
        message.attach(html_part)

        # Log in to server and send email
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                ssl_context: ssl.SSLContext = ssl.create_default_context()
                server.starttls(context=ssl_context)  # Secure the connection
                server.login(sender_addr, sender_password)
                failed_recipients: Dict[str, Tuple[int, str]] = server.sendmail(
                    sender_addr, to_addr, message.as_string())
                if not failed_recipients:
                    # TODO: write an info message
                    pass
                else:
                    # TODO: write a warning message
                    pass

        except Exception as ex:
            # TODO: write an error message
            raise


class GmailDeliverer(EmailDeliverer):
    """ GmailDeliverer is an EmailDeliverer customized for GMail """
    # GMail SMTP host and port settings
    host: ClassVar[str] = 'smtp.gmail.com'
    port: ClassVar[int] = 587  # For gmail with starttls

    def __init__(self):
        super().__init__(self, GmailDeliverer.host, GmailDeliverer.port)


if __name__ == '__main__':
    username: str = os.environ['USER'].replace('CORP\\', '')  # Delete Amazon junk
    sender: str = f'{username}.python.bootcamp@gmail.com'
    # For GMail, you'll need to enable "Allow less secure apps" in the sender's
    # GMail account settings (because we're not using OAuth for sign-in)
    password: str = '824HZ_k2Pan7iH'
    receiver: str = f'{username}@sutterhealth.org'

    time: str = dt.now().strftime('%A %b %w, %Y at %-I:%M %p')

    subj: str = 'Email from Python program'

    plain_msg: str = f"""\
        This is a plain text message from a Python application,
        sent at {time}

        No formatting of any kind."""

    html_msg: str = f"""\
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

    deliverer = GmailDeliverer()
    deliverer.send(sender, password, receiver, subj, plain_msg, html_msg)
