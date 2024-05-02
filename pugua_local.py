import configparser
import pathlib
from pathlib import Path
import csv
import sys

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
file = './logs-1.log'

if len(sys.argv) >1:
    file = sys.argv[1]

if __name__ == '__main__':
    with open(file, "r") as file:
        x = []
        for line in file.readlines():
            lss = line.split('|')
            if len(lss) <3:
                x[0] += line.replace("\n", "")
            else:
                d = lss[0]
                c = lss[2]
                if not c.startswith('{'):
                    x.append(d.split(',')[0])
                    x.append(c.replace("\n", ""))
                    print(c.replace("\n", ""))
                else:
                    x.append(d.split(',')[0])
                    x.append(c.replace("\n", ""))
                    output.append(x)
                    x = []
                #print(c.replace("\n", ""))
    #print(len(output))
    #print('\n'.join(map(str,output)))
    if config['csv']['csv']:
        with open(config['csv']['directory']+'/test.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerows(output)
            f.close()
