import smtplib, ssl, sys, getopt
import ntpath
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta

def send_email(pwd, path, rsgc, prod, to_email, cc_email, verbose_mode):
  # datetime object containing current date and time
  now = datetime.now()
  short_date_string = now.strftime("%Y-%m-%d")
  long_date_string = now.strftime("%A, %B %d, %Y")

  if rsgc:
    subject = "Rancho Sierra Golf Course Reservation Times for " + long_date_string
    link = '<a href="http://ranchosierragolfcourse.com/bookings/rsgc_' + short_date_string + '.html">here</a>'
    html = """\
    <html>
      <body>
        <div style="font-size:14px;color:darkgreen;">
        <p>Attached are the tee times for Rancho Sierra Golf Course for the next 7 days. You can also view this booking report by clicking """ +  link  + """\
          .</p><p>Have a very nice day.</p><br /><br />Michele
        </p>
        </div>
      </body>
    </html>
    """
  else:
    subject = "Desert Aire Golf Course Reservation Times for " + long_date_string
    link = '<a href="http://ranchosierragolfcourse.com/bookings/dagc_' + short_date_string + '.html">here</a>'
    html = """\
    <html>
      <body>
        <div style="font-size:14px;color:DodgerBlue;">
        <p>Attached are the tee times for Desert Aire Golf Course for the next 7 days. You can also view this booking report by clicking """ +  link  + """\
          .</p><p>Have a very nice day.</p><br /><br />Michele
        </p>
        </div>
      </body>
    </html>
    """
  text = "I hope things are going great for you today.\n\n"
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  port = 465  # For SSL
  sender_email = "michele@ranchosierragolfcourse.com" # "admin@avgolf-teetimes.com"
  password = pwd

  if prod:
    smtp_server = "mail.ranchosierragolfcourse.com"
  else:
    smtp_server = "mail.avgolf-teetimes.com"

  if to_email == None:
    to_email = "tim@timaiken.com@gmail.com"

  if cc_email == None:
    cc_email = "taaiken@gmail.com"

  if verbose_mode:
    print("to_email:", to_email)
    print("cc_email:", cc_email)

  # Create a multipart message and set headers
  #message = MIMEMultipart()
  message = MIMEMultipart("alternative")
  message["From"] = sender_email
  message["To"] = to_email
  message["Subject"] = subject
  message["Cc"] = cc_email             # Recommended for mass emails

  # Add body to email
  message.attach(MIMEText(text, "plain"))
  message.attach(MIMEText(html, "html"))

  filename = ntpath.basename(path)

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
  email_recipients = [to_email, cc_email]

  # Log in to server using secure context and send email
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
      server.login(sender_email, password)
      server.sendmail(sender_email, email_recipients, text)



