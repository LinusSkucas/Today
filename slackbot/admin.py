from django.contrib import admin
from .models import SlackUser, SlackWorkspace

admin.site.register(SlackUser)
admin.site.register(SlackWorkspace)
