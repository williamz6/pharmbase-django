from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('drugs/', views.getDrugs),
    path('drugs/<str:pk>/', views.getDrug),
    path('orders/', views.getOrders),
]