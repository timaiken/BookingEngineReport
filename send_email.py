import smtplib, ssl, sys, getopt
import ntpath
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def send_email(pwd, path, rsgc, prod, recipient):
  # datetime object containing current date and time
  now = datetime.now()
  short_date_string = now.strftime("%Y-%m-%d")
  long_date_string = now.strftime("%A, %B %d, %Y")

  if rsgc:
    subject = "Rancho Sierra Golf Course Reservation Times for " + long_date_string
    body = "Attached are the tee times for Rancho Sierra Golf Course for the next seven days.\n\nHave a good day.\n\nMichele\n" 
  else:
    subject = "Desert Aire Golf Course Reservation Times for " + long_date_string
    body = "Attached are the tee times for Desert Aire Golf Course for the next seven days.\n\nHave a good day.\n\nMichele\n" 

  port = 465  # For SSL
  sender_email = "michele@ranchosierragolfcourse.com" # "admin@avgolf-teetimes.com"
  password = pwd

  if prod:
    smtp_server = "mail.ranchosierragolfcourse.com"
  else:
    smtp_server = "mail.avgolf-teetimes.com"

  if recipient != None:
    receiver_email = recipient
  elif rsgc:
    receiver_email = "ranchosierragc@gmail.com"
  else:
    receiver_email = "desertairegc@gmail.com"

  print("receiver_email:", receiver_email)

  # Create a multipart message and set headers
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = subject
  message["Bcc"] = "tim@timaiken.com"  # Recommended for mass emails

  # Add body to email
  message.attach(MIMEText(body, "plain"))

  filename = ntpath.basename(path)
  #if rsgc:
  #  filename = "rsgc_" + short_date_string + ".csv"
  #else:
  #  filename = "dagc_" + short_date_string + ".csv"

  #if prod:
  #  pathname = "/home3/rsgcmgmt/data/prod/" + filename
  #else:
  #  pathname = "/home3/rsgcmgmt/data/" + filename

  # Open PDF file in binary mode
  with open(path, "rb") as attachment:
      # Add file as application/octet-stream
      # Email client can usually download this automatically as attachment
      part = MIMEBase("application", "octet-stream")
      part.set_payload(attachment.read())

  # Encode file in ASCII characters to send by email    
  encoders.encode_base64(part)

  val="attachment; filename=" + filename
  # Add header as key/value pair to attachment part
  part.add_header(
      "Content-Disposition",
      val
  #    f"attachment; filename={filename}"
  )

  # Add attachment to message and convert message to string
  message.attach(part)
  text = message.as_string()

  # Log in to server using secure context and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, receiver_email, text)


