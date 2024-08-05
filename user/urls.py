from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.signin, name="login"),
    path("register/", views.signup, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.account_view, name="account"),
    path("edit-account/", views.edit_account, name="edit-account"),
    path("drugs", views.drug, name="drugs"),
    path("drugs/order/", views.create_order, name="order-drug"),
    path("orders", views.orders, name="orders"),
    path("order-success", views.orderSuccess, name="order-success"),
]
