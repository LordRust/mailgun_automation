#!/usr/bin/env python3
import requests
import csv
import datetime
import os
import sys

env=os.path.expanduser(os.path.expandvars('$HOME/.config/python-private'))
sys.path.insert(0, env)
from secret import trinning_mailgun_key

key = trinning_mailgun_key
print(key)
exit

domain = 'trinning.se'
subject = 'Folkmusik med Trinning'
# html_file = open("sommarmail.html","r")
# html_template = html_file.read()
# html_file.close()
# text_file = open("sommarmail.txt","r")
# text_template = text_file.read()
# text_file.close()
log = open("./log/log_" + '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now()) + ".txt","w")

def sendmail(recipient, first_name, subject, text, html):
    request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(domain)
    request = requests.post(request_url, auth=('api', key), data={
        'from': 'Trinning Folkmusik <kontakt@trinning.se>',
        'to': recipient,
        'subject': subject,
        'text': text,
        'html': html
        },
        files=[("inline", open("trinning.jpg","rb")), ("inline", open("3fiol.jpg","rb"))]
    )
    log.write("".join(['Status: {0}'.format(request.status_code), "\n"]))
    log.write("".join(['Body:   {0}'.format(request.text), "\n\n"]))

with open("adresslista.csv", newline='') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.__next__() # pop of the header
    mottagare = []
    for row in reader:
        # print(row[4])
        # print(row[5])
        # print(">",row[6],"<")
        # print(">",row[7],"<")
        recipient = row[4].strip()
        first_name = row[2].strip()
        if row[4] not in mottagare and row[5] != "x" and row[7].strip() == "":
            mottagare.append(row[4].strip())
            with open('./utskick/'+row[5]+'.html') as f:
                html_template = f.read()
            with open('./utskick/'+row[5]+'.txt') as f:
                text_template = f.read()
            html = html_template.replace("%FIRSTNAME%",first_name)
            text = text_template.replace("%FIRSTNAME%",first_name)
            log.write("".join(["Skickat\t", recipient, "\t", first_name, "\t", row[5], "\n"]))
            sendmail(recipient, first_name, subject, text, html)
            #print("Till: ", recipient, "\nFirst: ", first_name, "\nÄmne: ", subject, "\nText:\n", text, "\nhtml:\n", html, sep="")
        else:
            log.write("".join(["Inte Skickat\t", recipient, "\t", first_name, "\n\n"]))
    #print(mottagare)
log.close()
