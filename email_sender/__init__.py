from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import smtplib

class EmailSender:
    def __init__(self, *, author, sender_email, password, subject, body):
        self._author = author
        self._sender_email = sender_email
        self._password = password
        self._subject = subject
        self._body = body
        self._targets = list()
        self._attachs = list()
            
    def add_target(self, email):
        self._targets.append(email)
        
    def add_attachment(self, attachment_path):
        self._attachs.append(attachment_path)
    
    def send(self):
        if len(self._targets) == 0:
            print('No targets have been added.')
        else:
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            attachment_packages = list()
            for attach in self._attachs:  # Package the attachments encoded in binary form.
                attachment = open(attach, 'rb')
                attachment_package = MIMEBase('application', 'octet-stream')
                attachment_package.set_payload(attachment.read())
                encoders.encode_base64(attachment_package)
                attachment_package.add_header('Content-Disposition', 'attachment; filename= ' + attach.split('/')[-1])
                attachment_packages.append(attachment_package)
            smtp = smtplib.SMTP(
                host=smtp_server,
                port=smtp_port
            )
            smtp.starttls()
            smtp.login(
                self._sender_email,
                self._password
            )
            for target in self._targets:
                msg = MIMEMultipart()
                msg['from'] = self._author
                msg['to'] = target
                msg['subject'] = self._subject
                msg.attach(MIMEText(self._body))  # Add the body.
                for attachment_package in attachment_packages:  # Add the attachments if any.
                    msg.attach(attachment_package)
                # smtp.send_message(msg)
                smtp.sendmail(self._sender_email, target, msg.as_string())
                print(f'E-mail sent from <{self._sender_email}> to <{target}>')
            smtp.quit()
            