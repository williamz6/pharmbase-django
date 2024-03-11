from django.db import models
from django.contrib.auth.models import User
from functools import wraps
from django.utils import timezone
from django.http import HttpResponseForbidden


# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("store_keeper", "Store Keeper"),
        ("guest", "Guest"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    roles = models.CharField(max_length=20, choices=ROLE_CHOICES, default="guest")
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    @classmethod
    def get_user_role(user):
        try:
            user_role = Profile.objects.get(user=user)
            return user_role.roles
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def has_permission(perm_name):
        def decorator(view_func):
            @wraps(view_func)
            def _wrapped_view(request, *args, **kwargs):
                if request.user.is_authenticated:
                    user_role = Profile.get_user_role(request.user)
                    if (
                        user_role
                        and user_role.permissions.filter(name=perm_name).exists()
                    ):
                        return view_func(request, *args, **kwargs)
                    else:
                        return HttpResponseForbidden(
                            "You don't have permission to perform this action"
                        )

            return _wrapped_view

        return decorator
