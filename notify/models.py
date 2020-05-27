from django.db import models
from django.contrib.auth.models import User
from timezone_field import TimeZoneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = TimeZoneField(blank=True, null=True)
    notification_time = models.TimeField(default=time(hour=7), blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
