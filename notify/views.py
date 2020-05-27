from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from slackbot.notify import send_notification
from slackbot.models import SlackUser


@api_view(["POST"])
def mark(request):
    data = request.POST
    users = SlackUser.objects.filter(slack_timezone=data['new_timezone'])
    for user in users:
        send_notification(user.slack_id)
    return Response(status=status.HTTP_200_OK)
