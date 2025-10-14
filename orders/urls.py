# MusShop/orders/urls.py
from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("create/", views.order_create, name="create"),
    path("success/<int:pk>/", views.order_success, name="success"),
]
