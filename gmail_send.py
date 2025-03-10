import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'nilabaust102@gmail.com'
email_password = 'gaih vjfq zelf zxey'
email_receiver = 'nilab102@gmail.com'

# Set the subject and body of the email
subject = 'testing email sending'
body = """
Testiiiiing email sending from Python.
This is the body of the email.
"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

# Add SSL (layer of security)
context = ssl.create_default_context()
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(email_sender, email_password)
    server.sendmail(email_sender, email_receiver, em.as_string())
