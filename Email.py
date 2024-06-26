import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def Sending_Receipt_Using_Email(recipient_email,file):
 
    sender_email = 'adimugeera@gmail.com'  # Your email address
    sender_password = 'abxg flfz kwne bfsg'  # Your email password
    subject = 'Receipt from Inventory Management System'

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach PDF file
    attachment = open(file, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {file}")
    msg.attach(part)

    # Login to SMTP server and send email
    smtp_server = 'smtp.gmail.com'  # Your SMTP server, e.g., for Gmail use 'smtp.gmail.com'
    smtp_port = 587  # Your SMTP port, e.g., for Gmail use 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, msg.as_string())
    server.quit()
