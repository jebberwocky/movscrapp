import configparser
from email.message import EmailMessage
import pathlib
from pathlib import Path
import smtplib, ssl

path: Path = pathlib.Path(__file__).parent.resolve()
config = configparser.ConfigParser()
#print(str(path)+'/default.ini')
config.read(str(path)+'/default.ini')
stage = config['env']['stage']
debug = config['env']['debug']
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = config['email']['sender'] # Enter your address
receiver_email = config['email']['to']  # Enter receiver address
password = config['email']['apppwd'] 
output = []

if __name__ == '__main__':
    with open(str(path)+"/c.txt", "r") as file:
        contents = file.read()

    msg = EmailMessage()
    msg.set_content(contents)
    msg['Subject'] = "🐕"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    #only sending email in production
    if stage == 'production' and  config['email']['email'] :
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email.split(","))