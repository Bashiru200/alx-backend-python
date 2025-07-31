from django.db import models
from django.conf import settings

class Message(models.Models):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)


qs = Message.objects.filter(parent_message__isnull=True) \
    .select_related('sender', 'receiver') \
    .prefetch_related('replies__sender', 'replies__receiver', 'replies__replies')

def build_threaded(message):
    by_parent = {}
    for msg in message:
        by_parent.setdefault(msg.parent_message_id, []).append(msg)

        def recurse(parent_id=None):
            thread = []
            for msg in by_parent.get(parent_id, []):
                thread.append({
                    'message': msg,
                    'replies': recurse(msg.id)
                })
            return thread
    return recurse(None)