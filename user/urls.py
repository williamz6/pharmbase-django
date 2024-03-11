from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.signin, name="login"),
    path("register", views.signup, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("account", views.account_view, name="account"),
]
