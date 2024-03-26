#!/usr/bin/env python3
# Uses the Mailgun API to save logs to JSON file
# Set environment variables MAILGUN_API_KEY and MAILGUN_SERVER
# Optionally set MAILGUN_LOG_DAYS to number of days to retrieve logs for
# Based on https://stackoverflow.com/a/49825979
# See API guide https://documentation.mailgun.com/en/latest/api-intro.html#introduction
import os
import json
import requests
import sys
from datetime import datetime, timedelta
from email import utils

DAYS_TO_GET = os.environ.get("MAILGUN_LOG_DAYS", 7)
MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
MAILGUN_SERVER = os.environ.get("MAILGUN_SERVER")

env=os.path.expanduser(os.path.expandvars('$HOME/.config/python-private'))
sys.path.insert(0, env)
from secret import trinning_mailgun_key

MAILGUN_API_KEY = trinning_mailgun_key

MAILGUN_SERVER = 'trinning.se'


if not MAILGUN_API_KEY or not MAILGUN_SERVER:
    print("Set environment variable MAILGUN_API_KEY and MAILGUN_SERVER")
    exit(1)

ITEMS_PER_PAGE = 300  # API is limited to 300

def get_logs(start_date, next_url=None):
    if next_url:
        print(f"Getting next batch of {ITEMS_PER_PAGE} from {next_url}...")
        response = requests.get(next_url,auth=("api", MAILGUN_API_KEY))
    else:
        url = 'https://api.mailgun.net/v3/{0}/events'.format(MAILGUN_SERVER)
        start_date_formatted = utils.format_datetime(start_date)  # Mailgun wants it in RFC 2822
        print(f"Getting first batch of {ITEMS_PER_PAGE} from {url} since {start_date_formatted}...")
        response = requests.get(
            url,
            auth=("api", MAILGUN_API_KEY),
            params={"begin"       : start_date_formatted,
                    "ascending"   : "yes",
                    "pretty"      : "yes",
                    "limit"       : ITEMS_PER_PAGE,}
#                    "event"       : "accepted",}
        )
    response.raise_for_status()
    return response.json()


start = datetime.now() - timedelta(DAYS_TO_GET)
log_items = []
current_page = get_logs(start)

while current_page.get('items'):
    items = current_page.get('items')
    log_items.extend(items)
    print(f"Retrieved {len(items)} records for a total of {len(log_items)}")
    next_url = current_page.get('paging').get('next', None)
    current_page = get_logs(start, next_url=next_url)

file_out = f"mailgun-logs-{MAILGUN_SERVER}_{start.strftime('%Y-%m-%d')}_to_{datetime.now().strftime('%Y-%m-%d')}.json"
print(f"Writing out {file_out}")
with open(file_out, 'w') as file_out_handle:
    json.dump(log_items, file_out_handle, indent=4)

print("Done.")
