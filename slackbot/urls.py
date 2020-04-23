"""URLS for the slackbot"""
from django.urls import path

from . import views

urlpatterns = [
    # Commands
    path('commands/today', views.today_command, name="today"),
    # path('events', )
]