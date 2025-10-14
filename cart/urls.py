# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<slug:slug>/", views.add_to_cart, name="cart_add"),
    path("remove/<slug:slug>/", views.remove_from_cart, name="cart_remove"),
    path("clear/", views.clear_cart, name="cart_clear"),
]
