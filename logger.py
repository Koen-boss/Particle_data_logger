import serial
import time
from datetime import datetime
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#file location and name
filePath = f"/home/kotamech/Desktop/log.txt" #filepath to log
fileName = f"log.txt"

#starting serial 
ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1) #intitializing serial
time.sleep(2) #waiting for serial to start

#Email text
subject = "DCCA user data"
text = "Hello, Included is the usage data of the DCCA chestnut treatment sets of today"

# Email configuration
SMTPServer = "smtp.gmail.com"
SMTPPort = 587
senderEmail = "userdatatreehold@gmail.com"  # Replace with your email
emailPassword = "bpbc hufi dvqd fbjt"  # Replace with your password or App Password
receiverEmail = "koen@kotamech.com" #receiver email

def send_email(senderEmail, receiverEmail, emailPassword, SMTPServer, SMTPPort, subject, text, filePath):
    # Create the email
    msg = MIMEMultipart()
    msg["From"] = senderEmail
    msg["To"] = receiverEmail  # Replace with the recipient's email
    msg["Subject"] = subject

    # Email body
    body = text
    msg.attach(MIMEText(body, "plain"))

    
        # **Attach a File**
    filename = fileName  # Replace with the file you want to attach
    try:
        with open(filePath, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())  # Read the file in binary mode

        encoders.encode_base64(part)  # Encode file to base64
        part.add_header(
            "Content-Disposition", f"attachment; filename={filename}"
        )
        msg.attach(part)  # Attach the file to the email
    except Exception as e:
        print(f"Error attaching file: {e}")

    # Send the Email
    try:
        server = smtplib.SMTP(SMTPServer, SMTPPort)
        server.starttls()  # Secure the connection
        server.login(senderEmail, emailPassword)
        server.sendmail(receiverEmail, msg["To"], msg.as_string())
        server.quit()
        print("Email sent successfully with attachment!")
    except Exception as e:
        print(f"Error sending email: {e}")


#main loop
while True:
    #check for incoming serial
    if ser.in_waiting >0:
        line = ser.readline().decode('utf-8', errors = 'replace').strip()
        print("received", line)
        with open(filePath, "a") as file:
            writeLine = line +" | " + str(datetime.now()) + "\n"
            file.write(str(writeLine)) #write received data
          
    #send email at end of day    
    now = datetime.now()  
    if os.path.getsize(filePath) > 0 and now.hour == 23 and now.minute == 59:
        send_email(senderEmail, receiverEmail, emailPassword, SMTPServer, SMTPPort, subject, text, filePath) 
        open(filePath, "w").close() #clear file
        time.sleep(60)