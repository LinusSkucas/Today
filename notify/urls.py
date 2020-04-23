from django.urls import path

from . import views

urlpatterns = [
    # Notification from Lambda
    path('private/mark', views.mark, name="notification"),
]