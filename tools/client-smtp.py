#!/usr/bin/env python

import smtplib
import base64

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

filename = "attach.txt"

# Read a file and encode it into base64 format
fo = open(filename, "rb")
file_content = fo.read()
encoded_content = base64.b64encode(file_content)  # base64

sender = "sender@domain.com"
reciever = "reciever@domain.com"

msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = reciever
msg["Subject"] = "Python email"

body = """
This is a test email.
"""
msg.attach(MIMEText(body, "plain"))

try:
    smtpObj = smtplib.SMTP("mail.server", 2525)
    smtpObj.set_debuglevel(2)
    # smtpObj.starttls()
    smtpObj.login("USER", "PASS")
    smtpObj.sendmail(sender, reciever, msg.as_string())
    print("Successfully sent email")
except Exception:
    print("Error: unable to send email")
