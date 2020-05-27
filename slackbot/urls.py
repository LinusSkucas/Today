"""URLS for the slackbot"""
from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [
    # Commands and Events
    path('api/', include('slack_utils.urls')),
    path('today/', views.today_command),
    path('interaction', views.interaction),
    path('auth', views.redirect_auth),
    path('auth/redirect', views.redirect_auth)
]