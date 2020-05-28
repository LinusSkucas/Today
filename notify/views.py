from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from slackbot.notify import send_notification
from slackbot.models import SlackUser

with open("hourMarkCallerLambda/shared_secret.txt", 'r') as file:
    shared_secret = file.read()


@api_view(["POST"])
def mark(request):
    data = request.POST
    auth_secret = data.get('Authorization')
    if auth_secret == shared_secret:
        users = SlackUser.objects.filter(slack_timezone=data['new_timezone'])
        for user in users:
            send_notification(user.slack_id, user.slack_workspace.slack_bot_user_token)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return Response(status=status.HTTP_200_OK)
