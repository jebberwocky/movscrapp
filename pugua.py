import configparser
from email.message import EmailMessage
import pathlib
from pathlib import Path
import smtplib, ssl
import csv

path: Path = pathlib.Path(__file__).parent.resolve()
config = configparser.ConfigParser()
#print(str(path)+'/default.ini')
config.read(str(path)+'/default.ini')
stage = config['env']['stage']
debug = config['env']['debug']
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = config['email']['sender'] # Enter your address
receiver_email = config['pugua']['to']  # Enter receiver address
password = config['email']['apppwd']
logfiles = config['pugua']['log'].split(',')
csvfile = config['pugua']['csv']
output = []

if __name__ == '__main__':
    for logfile in logfiles:
        _o = []
        with open(logfile, "r") as file:
            x = []
            for line in file.readlines():
                a = line.split('|')
                if len(a) <3:
                    x[0] += line.replace("\n", "")
                else:
                    c = a[2]
                    if not c.startswith('{\'res'):
                        x.append(a[0])
                        x.append(c.replace("\n", ""))
                    else:
                        x.append(c.replace("\n", ""))
                        _o.append(x)
                        x = []
            print(logfile+":"+str(len(_o)))
            output = output + _o

    if config['csv']['csv']:
        with open(csvfile, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(output)
            f.close()

    contents = 'count: ' + str(len(output))
    #contents =  '<div>count: ' + str(len(output))+"</div><div><a href='http://dl.colbt.cc/csv/data.csv'>download data</a></div>"
    msg = EmailMessage()
    #msg.set_content(contents,subtype="html")
    msg.set_content(contents)
    msg['Subject'] = "👋"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    #stop attaching original log to avoid exceeding mail limit
    #for logfile in logfiles:
    #    with open(logfile, 'rb') as content_file:
    #       content = content_file.read()
    #        msg.add_attachment(content, maintype='application', subtype='txt', filename='logfile')
    with open(csvfile, 'rb') as content_file:
        content = content_file.read()
        msg.add_attachment(content, maintype='application', subtype='csv', filename='data.csv')
    #only sending email in production
    if stage == 'production' and  config['email']['email'] :
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email.split(","))
