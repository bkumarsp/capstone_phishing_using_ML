# New mail service | author: Bharath
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import smtplib

from aquaphish.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_HOST
import os

#########################################

# TODO: Check if email service works



# email message construct utility
def message(subject="Python Notification", text="", img=None, attachment=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject  
    msg.attach(MIMEText(text))  

    if img is not None:
        if type(img) is not list:  
            img = [img] 

        for one_img in img:
            img_data = open(one_img, 'rb').read()  
            msg.attach(MIMEImage(img_data, name=os.path.basename(one_img))) #provide image in current folder
  
   
    if attachment is not None:
        if type(attachment) is not list:
            attachment = [attachment]  
  
        for one_attachment in attachment:
            with open(one_attachment, 'rb') as f:
                file = MIMEApplication( f.read(),   name=os.path.basename(one_attachment) )

            file['Content-Disposition'] = f'attachment;\
                filename="{os.path.basename(one_attachment)}"'
              
            msg.attach(file)
    return msg



# New mail micro service
def smtpMail_microservice(
                            emailFrom="capstone.aquaphish20@gmail.com", 
                            emailTo = ["bhuvantejreddy45@gmail.com", "adityahegde0011@gmail.com", "srvyshak@gmail.com", "bkumarsp6@gmail.com"],
                            emailSubject = "Capstone Team 20",
                            emailBody = "Say hello to our capstone phishing mail service. Launched using python and SMTP."                  
                        ):
    # initialize connection
    smtp_port = EMAIL_PORT
    smtp_server = EMAIL_HOST

    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.ehlo()
    smtp.starttls()

    # Login using app gmail credentials
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    email_message = message(emailSubject, emailBody)

    smtp.sendmail(from_addr= emailFrom, to_addrs= emailTo, msg= email_message.as_string())
    smtp.quit()

    return "success"