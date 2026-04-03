from django.urls import path
from .views import chat_respond

urlpatterns = [
    path('respond/', chat_respond, name='chat_respond'),
]
