# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
# from django.contrib import messages
# from django.http import get_user_model
# from .models import Message, UnreadMessagesManager
# from utils import build_threaded

# User = get_user_model()

# @login_required
# def delete_user(request):
#     user = request.user
#     user.delete()
#     messages.success(request, "Your account and all associated data have been deleted.")
#     return redirect('home')

# def conversation_view(request, conversation_owner):
#     root_msgs = Message.objects.filter(receiver=conversation_owner, parent_message__isnull=True) \
#         .select_related('sender', 'receiver') \
#         .prefetch_related('replies__sender', 'replies__receiver', 'replies__replies')
#     all_msgs = Message.objects.filter(receiver=conversation_owner) \
#         .select_related('sender', 'receiver') \
#         .prefetch_related('replies')
#     thread = bulid_threaded(root_msgs)
#     return render(request, 'chat/threaded.html', {'thread' : thread})

# def unreadmessages(request):
#     unread_messages = UnreadMessagesManager().get_queryset()
#     return render(request, 'chat/unread_messages.html', {'unread_messages': unread_messages})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from .models import Message
from .utils import build_threaded  # fix spelling and import appropriately
from django.views.decorators.cache import cache_page

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account and all associated data have been deleted.")
    return redirect('home')

@login_required
def conversation_view(request, conversation_owner):
    root_msgs = Message.objects.filter(receiver=conversation_owner, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies__sender', 'replies__receiver', 'replies__replies')
    thread = build_threaded(root_msgs)
    return render(request, 'chat/threaded.html', {'thread': thread})

@login_required
def unreadmessages(request):
    unread_messages = Message.unread.unread_for_user  # Make sure the manager is defined on the model
    return render(request, 'chat/unread_messages.html', {'unread_messages': unread_messages})

# cache_page decorator to cache the response for 60 seconds
@cache_page(60)
def convrsation_messages(request, conversation_pk):
    #fetch messages for a specific conversation
    message = Message.objects.filter(conversation_id=conversation_pk).order_by('sent_at')
    return render(request, 'conversations/messages.html', {'messages': messages})