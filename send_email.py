import smtplib
import ssl
from email.message import EmailMessage

# Define email sender and receiver
email_sender = 'nilabaust102@gmail.com'
email_password = ''
email_receiver = 'nilab102@gmail.com'

# Set email subject
subject = 'Employment Offer Letter'

# Read HTML content from file
html_file_path = r'./offer_letter.html'

with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Create EmailMessage object
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject

# Add HTML content
em.add_alternative(html_content, subtype='html')

# Send email with SSL
context = ssl.create_default_context()
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(email_sender, email_password)
    server.send_message(em)