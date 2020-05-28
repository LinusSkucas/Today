from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from slack import WebClient
from slack_utils.signals import event_received
from django.dispatch import receiver
from django.conf import settings
from .models import SlackWorkspace
import requests
import json
import random
from . import verify
from . import notify
from .message_matching import identify_message, MessageIntent
from .modal_configuration import *


@api_view(["POST"])
def today_command(request):
    verify.verify_request(request)
    data = request.data
    user_id = data.get('user_id')
    action = data.get('text')
    response_url = data.get('response_url')
    action = identify_message(action)
    workspace_id = data.get('team_id')
    workspace_token = SlackWorkspace.objects.get(pk=workspace_id).slack_bot_user_token
    if action == MessageIntent.ENROLL:
        notify.enroll_notifications(user_id, response_url, workspace_token, workspace_id)
    elif action == MessageIntent.STOP:
        notify.disable_notifications(user_id, response_url, workspace_token)
    else:
        message = notify.format_notification(user_id, workspace_token)
        requests.post(response_url, json={"text": message, 'response_type': 'in_channel'})


    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def interaction(request):
    verify.verify_request(request)

    data = json.loads(request.data.get('payload'))
    interaction_type = data.get('type')
    trigger_id = data.get("trigger_id")
    workspace_id = data.get('team').get('id')
    workspace_token = SlackWorkspace.objects.get(pk=workspace_id).slack_bot_user_token
    client = WebClient(token=workspace_token)
    if interaction_type == 'shortcut' or interaction_type == 'message_action':
        # Is a shortcut payload
        shortcut = data.get('callback_id')
        if shortcut == 'today_global_shortcut':
            message = SEND_DATE_TO_CHANNEL_GLOBAL_SHORTCUT
            message['private_metadata'] = '{"view": "date_global_shortcut"}'
            client.views_open(trigger_id=trigger_id, view=message)
        elif shortcut == 'enroll_global_shortcut':
            user_id = data['user']['id']
            notify.add_user_notifications(user_id, workspace_token, workspace_id)
            channel = client.conversations_open(users=user_id)['channel']['id']
            message = ":white_check_mark: Alright, from now on, at 7:00 AM your time, I'll send you the date!"
            client.chat_postMessage(channel=channel, text=message, username='Today\'s Date',
                                    icon_emoji=random.choice(notify.available_emoji))
        elif shortcut == 'stop_global_shortcut':
            user_id = data['user']['id']
            notify.delete_user_notifications(user_id, workspace_token)
            channel = client.conversations_open(users=user_id)['channel']['id']
            message = ":cry: I won't send you notifications about the day of the week ever again."
            client.chat_postMessage(channel=channel, text=message, username='Today\'s Date',
                                    icon_emoji="no_entry_sign:")
        elif shortcut == 'today_message_shortcut':
            if data.get('message').get('subtype') == 'bot_message':  # make sure this isn't a bot
                return Response(status.HTTP_200_OK)
            message = CORRECT_TODAY_MESSAGE_SHORTCUT_CONFIRM_MODEL
            message['blocks'][0]["text"]["text"] = "Are you sure that want to correct {}'s date?".format(
                client.users_info(user=data.get('message').get('user')).get('user').get('name'))

            message['private_metadata'] = json.dumps(
                {"payload": request.data.get('payload'), "view": "correction_view"})
            client.views_open(trigger_id=trigger_id, view=message)
    elif interaction_type == 'view_submission':
        metadata = json.loads(data.get('view').get('private_metadata'))
        view = metadata.get('view')
        if view == 'correction_view':
            payload = json.loads(metadata.get('payload'))
            ts = payload.get("message").get('ts')
            channel = payload.get("channel").get('id')
            client.conversations_join(channel=channel)
            client.chat_postMessage(channel=channel, thread_ts=ts,
                                    text=notify.format_notification(user_id=payload.get('message').get('user'),
                                                                    workspace_token=workspace_token),
                                    username='Today\'s Date Troll', icon_emoji=random.choice(notify.available_emoji))
        elif view == 'date_global_shortcut':
            response_url = data.get('response_urls')[0].get('response_url')
            user_id = data.get('user').get('id')
            message = notify.format_notification(user_id, workspace_token)
            requests.post(response_url, json={"text": message, 'response_type': 'in_channel'})
    elif interaction_type == 'block_actions':
        user_id = data.get('user').get('id')
        if data.get('actions')[0].get('type') == 'radio_buttons':
            radio_home_value = data.get('actions')[0].get('selected_option').get('value')
            if radio_home_value == 'enroll_notifications':
                notify.add_user_notifications(user_id, workspace_token, workspace_id)
            elif radio_home_value == 'disable_notifications':
                notify.delete_user_notifications(user_id, workspace_token)
        elif data.get('actions')[0].get('value') == 'update_timezone_home':
            # Force update new_timezone
            notify.update_timezone(user_id=user_id, workspace_token=workspace_token)

    return Response(status=status.HTTP_200_OK)


@receiver(event_received)
def on_event_received(sender, event_type, event_data, **kwargs):
    if event_type == 'app_home_opened' and event_data.get('tab') == 'home':
        # render app home!
        user_id = event_data.get('user')
        workspace_id = event_data.get('view').get('team_id')
        workspace_token = SlackWorkspace.objects.get(pk=workspace_id).slack_bot_user_token
        notify.publish_homepage(user_id=user_id, workspace_token=workspace_token)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def redirect_auth(request):
    """Check get auth code, change into access token"""
    code = request.GET.get('code')
    client = WebClient()
    resp = client.oauth_v2_access(client_id=settings.SLACK_CLIENT_ID, client_secret=settings.SLACK_CLIENT_SECRET,
                                  code=code)
    workspace = SlackWorkspace()
    workspace.slack_workplace_id = resp['team']['id']
    workspace.slack_bot_user_token = resp['access_token']
    workspace.save()
    return Response(status=status.HTTP_200_OK, data="added to slack!")


def generate_install_url(request):
    return Response(status=status.HTTP_200_OK,
                    data='''<a href="https://slack.com/oauth/v2/authorize?client_id=1053571365575.1066999652021&
                    scope=app_mentions:read,channels:join,channels:manage,channels:read,chat:write,
                    chat:write.customize,commands,groups:read,im:history,im:read,im:write,users:read">
                    <img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/
                    add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, 
                    https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>''')
