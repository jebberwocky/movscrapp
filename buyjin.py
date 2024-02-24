from lxml import html
import requests
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

def buyiju():
    url = "https://www.buyiju.com/bazi/yuncheng/"
    payload = 'year=1982&month=2&day=8&hour=3&sex=%E7%94%B7&action=test'
    headers = {
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'ASPSESSIONIDAUDRACSB=OIACBFHAAPIMOBLCIBJCKNJB; ASPSESSIONIDAUDTACTA=NOCBMKNACKDNCFDEDJGPJNNL; day=8; hour=3; month=2; sex=%E7%94%B7; year=1982'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


if __name__ == '__main__':
    contents = buyiju()
    msg = EmailMessage()
    msg.set_content(contents)
    msg.add_alternative(contents, subtype='html')
    msg['Subject'] = "🐕🐕🐕"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    #only sending email in production
    if stage == 'production' and  config['email']['email'] :
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email.split(","))
