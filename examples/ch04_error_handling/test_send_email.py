from os import environ
import smtplib
import ssl
from datetime import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from textwrap import dedent
from typing import Optional, Dict, Tuple
from unittest import TestCase


class SendEmailTest:
    username: str = environ['USER'].replace('CORP\\', '')
    sender_email: str = f'{username}.python.bootcamp@gmail.com'
    # For GMail, you'll need to enable "Allow less secure apps" in the sender's
    # GMail account settings (because we're not using OAuth for sign-in)
    sender_password: str = '824HZ_k2Pan7iH'
    receiver_email: str = f'{username}@sutterhealth.org'

    # for GMail
    smtp_host: str = 'smtp.gmail.com'
    smtp_port: int = 587  # For gmail with starttls

    # for local SMTP debugging server
    smtp_host_debug: str = 'localhost'
    smtp_port_debug: int = 1025

    def test_send_unsecured_email(self):
        # Launch debug SMTP server:
        # python -m smtpd -c DebuggingServer -n localhost:1025

        message: str = f"""\
            Subject: Hello from Python

            This message was sent from Python at {dt.now()}."""

        # Log in to server and send emails
        server: Optional[smtplib.SMTP] = None
        failed_recipients: Dict[str, Tuple[int, str]] = {}
        try:
            server: smtplib.SMTP = smtplib.SMTP(self.smtp_host_debug,
                                                self.smtp_port_debug)

            # Send email
            failed_recipients = server.sendmail(
                self.sender_email, self.receiver_email, dedent(message))

            # if sendmail() returns a Dict with items for each failed recipient.
            # An item's key is the recipient, and the value is tuple of the
            # SMTP error code and SMTP error message.
            assert not failed_recipients

        except Exception as e:
            print(e)  # Print any error messages to stdout
            print(f'failed recipients: {failed_recipients}')
            raise  # Re-raise exception
        finally:
            if server:
                server.quit()

    def test_send_secured_email(self):
        message = """\
            Subject: Hello from Python

            This message is sent from Python."""

        # Create a secure SSL context
        ssl_context: ssl.SSLContext = ssl.create_default_context()

        # Log in to server and send email
        server: Optional[smtplib.SMTP] = None
        failed_recipients: Dict[str, Tuple[int, str]] = {}
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls(context=ssl_context)  # Secure the connection
            server.login(self.sender_email, self.sender_password)

            # Send email
            failed_recipients = server.sendmail(
                self.sender_email, self.receiver_email, dedent(message))

            assert not failed_recipients

        except Exception as e:
            print(e)  # Print any error messages to stdout
            print(f'failed recipients: {failed_recipients}')
            raise  # Re-raise exception
        finally:
            if server:
                server.quit()

    def test_send_secured_html_email(self):
        plain_message: str = """\
            This is a plain text message from a Python application.
            
            No formatting of any kind."""

        html_message: str = f"""\
            <html>
                <body>
                    <h1>Message from Python Application</h1>
                    <p>This is an HTML message</p>
                    <p>It supports the usual HTML features:</p>
                    <ul>
                        <li>Different heading levels</li>
                        <li>Lists</li>
                        <li><a href='https://en.wikipedia.org/wiki/Hyperlink'>
                            Links</a></li>
                        <li>And the other features you know and love</li>
                    </ul>
                    <p>And dynamic message creation: 
                    this messages was sent at
                    {dt.now().strftime('%A, %b %w, %Y at %h:%m %p')}</p>
                </body>
            </html>"""

        message: MIMEMultipart = MIMEMultipart('alternative')
        message['Subject'] = 'Notification from Python app'
        message['From'] = self.sender_email
        message['To'] = self.receiver_email

        # Turn these into plain/html MIMEText objects
        plain_part: MIMEText = MIMEText(plain_message, 'plain')
        html_part: MIMEText = MIMEText(html_message, 'html')

        # Add HTML and plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(plain_part)
        message.attach(html_part)

        # Create a secure SSL context
        ssl_context: ssl.SSLContext = ssl.create_default_context()

        # Log in to server and send email
        server: Optional[smtplib.SMTP] = None
        failed_recipients: Dict[str, Tuple[int, str]] = {}
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls(context=ssl_context)  # Secure the connection
            server.login(self.sender_email, self.sender_password)

            # Send email
            failed_recipients = server.sendmail(
                self.sender_email, self.receiver_email, message.as_string())

            assert not failed_recipients

        except Exception as e:
            print(e)  # Print any error messages to stdout
            print(f'failed recipients: {failed_recipients}')
            raise  # Re-raise exception
        finally:
            if server:
                server.quit()
