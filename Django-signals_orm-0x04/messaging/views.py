from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import get_user_model
from .models import Message, UnreadMessagesManager

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account and all associated data have been deleted.")
    return redirect('home')

def conversation_view(request, conversation_owner):
    root_msgs = Message.objects.filter(receiver=conversation_owner, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies__sender', 'replies__receiver', 'replies__replies')
    all_msgs = Message.objects.filter(receiver=conversation_owner) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies')
    thread = bulid_threaded(root_msgs)
    return render(request, 'chat/threaded.html', {'thread' : thread}

def unreadmessages(request):
    unread_messages = UnreadMessagesManager().get_queryset()
    return render(request, 'chat/unread_messages.html', {'unread_messages': unread_messages})