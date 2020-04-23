import datetime
import json
import requests

url = "https://42fbb406.ngrok.io/private/mark"


def lambda_handler(event, context):
    requests.get(url=url)
    return {'statusCode': 200, }
