from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from slackbot.notify import send_notification

user = 'U012Q4A6WGG'


@api_view(["PUT"])
def mark(request):
    send_notification(user)
    return Response(status=status.HTTP_200_OK)
