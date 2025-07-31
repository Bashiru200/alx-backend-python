from django.db import models
from django.conf import settings

class Message(models.Models):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Notification(models.Models):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Models):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    change_type = models.CharField(max_length=50)
    change_timestamp = models.DateTimeField(auto_now_add=True)