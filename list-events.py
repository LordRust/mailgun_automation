#!/usr/bin/env python3
import requests
import csv
import os
import sys

env=os.path.expanduser(os.path.expandvars('$HOME/.config/python-private'))
sys.path.insert(0, env)
from secret import trinning_mailgun_key

key = trinning_mailgun_key

domain = 'trinning.se'

request_url = 'https://api.mailgun.net/v3/{0}/events'.format(domain)
request = requests.get(request_url, auth=('api', key), params={'limit': 5})

print('Status: {0}'.format(request.status_code))
print('Body:   {0}'.format(request.text))
