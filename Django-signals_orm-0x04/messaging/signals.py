from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    if instance.pk:
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                change_type='edited',
                edited_by=instance.sender,
                change_timestamp=instance.edited_at
            )

User = get_user_model()

@receiver(post_delete, sender=Message)
def delete_user(sender, instance, origin=None, **kwargs):
    if origin is None or not instance(origin, User):
        Message.objects.filter(sender=instance.sender).delete()
        pass