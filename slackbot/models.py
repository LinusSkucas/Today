from django.db import models
from notify.models import Profile
from timezone_field import TimeZoneField
from django.db.models.signals import post_save
from django.dispatch import receiver


class SlackWorkspace(models.Model):
    slack_workplace_id = models.CharField(max_length=500, unique=True, primary_key=True)
    slack_bot_user_token = models.CharField(max_length=500)


class SlackUser(models.Model):
    slack_workspace = models.ForeignKey(SlackWorkspace, on_delete=models.CASCADE)
    slack_id = models.CharField(max_length=500, primary_key=True)
    slack_enabled = models.BooleanField(null=True, blank=True)
    slack_timezone = TimeZoneField(null=True, blank=True)
    slack_timezone_override = models.BooleanField(null=True, blank=True)
