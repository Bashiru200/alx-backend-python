from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import get_user_model

User = get_user_model()

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account and all associated data have been deleted.")
    return redirect('home')