from slack import WebClient
from datecore import Date, DateFormat
from datetime import datetime
from pytz import timezone
import requests
from slackbot.models import SlackUser
from .modal_configuration import *
import random
import copy

available_emoji = [':alarm_clock', ':date:', ':calendar:', ':clock7:']


def publish_homepage(user_id, workspace_token):
    user = SlackUser.objects.filter(pk=user_id).first()
    client = WebClient(token=workspace_token)
    if not user:
        # Not has notifications
        user = client.users_info(user=user_id)['user']
        date = Date(date=datetime.now(tz=timezone(user['tz'])), date_format=DateFormat.NORMAL_YEAR)
        home_view = copy.deepcopy(TODAY_DISABLE_NOTIFICATIONS_APP_HOME)
        home_view['blocks'][1]['text']['text'] = date.nice_date
    else:
        user_timezone = user.slack_timezone.zone
        date = Date(date=datetime.now(tz=timezone(user_timezone)), date_format=DateFormat.NORMAL_YEAR)
        home_view = copy.deepcopy(TODAY_ENROLL_NOTIFICATIONS_HOME)
        home_view['blocks'][1]['text']['text'] = date.nice_date
        home_view['blocks'][7]['text']['text'] = home_view['blocks'][7]['text']['text'] + user_timezone
    client.views_publish(user_id=user_id, view=home_view)


def format_notification(user_id, workspace_token):
    client = WebClient(token=workspace_token)
    user = client.users_info(user=user_id)['user']
    date = Date(date=datetime.now(tz=timezone(user['tz'])))

    message = date.create_message(user=f"<@{user_id}>")
    return message


def send_notification(user_id, workspace_token):
    client = WebClient(token=workspace_token)
    channel = client.conversations_open(users=user_id)['channel']['id']
    message = format_notification(user_id, workspace_token)
    client.chat_postMessage(channel=channel, text=message, username='Today\'s Date',
                            icon_emoji=random.choice(available_emoji))


def add_user_notifications(user_id, workspace_token, workplace_id):
    """Adds user to db"""
    client = WebClient(token=workspace_token)
    user_info = client.users_info(user=user_id)['user']
    user, created = SlackUser.objects.get_or_create(slack_id=user_id, slack_workspace_id=workplace_id)
    user.slack_timezone = user_info['tz']
    user.slack_enabled = True
    user.slack_timezone_override = True
    user.save()
    publish_homepage(user_id, workspace_token=workspace_token)


def enroll_notifications(user_id, response_url, workspace_token, workspace_id):
    """Sends a response"""
    add_user_notifications(user_id, workspace_token, workspace_id)
    requests.post(response_url, json={
        "text": ":white_check_mark: Alright, from now on, at 7:00 AM your time, I'll send you the date!",
        'response_type': 'ephemeral', 'as_emoji': ':clock7:', 'username': 'Today'})


def delete_user_notifications(user_id, workspace_token):
    """Deletes user from db"""
    try:
        SlackUser.objects.get(slack_id=user_id).delete()
    except SlackUser.DoesNotExist:
        pass
    publish_homepage(user_id, workspace_token)


def disable_notifications(user_id, response_url, workspace_token):
    """Sends the response"""
    delete_user_notifications(user_id, workspace_token=workspace_token)
    requests.post(response_url, json={
        "text": ":cry: I won't send you notifications about the day of the week ever again.",
        'response_type': 'ephemeral'})


def update_timezone(user_id, workspace_token, new_timezone=None):
    client = WebClient(token=workspace_token)
    user = SlackUser.objects.filter(pk=user_id).first()
    if not new_timezone:
        new_timezone = client.users_info(user=user_id)['user']['tz']
    user.slack_timezone.zone = new_timezone
    user.save()
    publish_homepage(user_id, workspace_token)
