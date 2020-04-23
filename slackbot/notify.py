from slack import WebClient
from django.conf import settings
from datecore import Date
from datetime import datetime
from pytz import timezone

client = WebClient(token=settings.SLACK_BOT_USER_TOKEN)


def send_notification(user_id):
    channel = client.conversations_open(users=user_id)['channel']['id']
    user = client.users_info(user=user_id)['user']
    date = Date(date=datetime.now(tz=timezone(user['tz'])))

    message = date.create_message(user=f"<@{user_id}>")
    client.chat_postMessage(channel=channel, text=message)
