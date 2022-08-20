from django.contrib.auth import get_user_model
from .models import UserProfile
from django.shortcuts import get_object_or_404


def get_profile(request):
    user = get_user_model().objects.filter(username__icontains=request.user.get_username()).values('id')
    profile = get_object_or_404(UserProfile, user=user[0]['id'])
    return profile
