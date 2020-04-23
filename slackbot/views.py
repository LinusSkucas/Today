from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from slack import WebClient, errors
from django.conf import settings
from datecore import Date, DateFormat
from datetime import datetime
from pytz import timezone
import requests
from . import verify

client = WebClient(token=settings.SLACK_BOT_USER_TOKEN)


@api_view(["POST"])
def today_command(request):
    verify.verify_request(request)

    data = request.data
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    user = client.users_info(user=user_id)['user']
    date = Date(date=datetime.now(tz=timezone(user['tz'])))

    message = date.create_message(user=f"<@{user_id}>")
    client.conversations_join(channel=channel_id)
    client.chat_postMessage(channel=channel_id, text=message)
    return Response(status=status.HTTP_200_OK)
