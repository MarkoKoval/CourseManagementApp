import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time



def send_email_for_course_subscription(subscriber_name,coursename,subject,  message,reciever_email):
    email = 'mark.koval.ua@gmail.com'
    password = 'markkoval123'
    send_to_email = reciever_email
    #subject = 'New subscriber for the course congratulations'  # The subject line
   # message = subscriber_name +" "+" subscribed to your course "+coursename

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()  # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()
    print(time.time())

"""email = 'mark.koval.ua@gmail.com'
password = 'markkoval123'
send_to_email = 'marko.koval.pz.2016@lpnu.ua,mark.koval.ua@gmail.com'
subject = 'This is the subject' # The subject line
message = 'Hello'

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

 # Attach the message to the MIMEMultipart object
msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email, password)
text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
server.sendmail(email, send_to_email, text)
server.quit()
print(time.time())"""