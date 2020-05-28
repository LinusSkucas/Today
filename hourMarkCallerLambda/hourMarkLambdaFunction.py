import datetime
import pytz
import requests
import os

url = os.getenv('SERVER_URL')
with open('shared_secret.txt', 'r') as file:
    shared_secret = file.read()
notificationTime = datetime.time(hour=7)


def lambda_handler(event, context):
    for tz in pytz.all_timezones:
        if datetime.datetime.now(tz=pytz.timezone(tz)).hour == notificationTime.hour:
            requests.post(url, data={'new_timezone': tz, 'Authorization': shared_secret})
    return {'statusCode': 200}

