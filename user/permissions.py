from .models import * 
from django.http import HttpResponseForbidden
from functools import wraps

def get_user_role(user):
    user_role = Profile.objects.get(user=user)
    return user_role.roles

# def has_permissions