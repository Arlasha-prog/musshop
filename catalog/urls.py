from django.urls import path
from . import views

urlpatterns = [
    # Главная
    path("", views.home, name="home"),

    # Каталог (список всех товаров)
    path("properties/", views.all_products, name="shop_all"),
    path("properties.html", views.all_products),  # поддержка старой ссылки

    # Карточка товара
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("properties/<slug:slug>/", views.product_detail),  # старый вариант

    # Категории
    path("category/<slug:slug>/", views.category_list, name="category"),

    # Поиск
    path("search/", views.all_products, name="product_search"),

    # Универсальные страницы (about.html, contact.html и т.д.)
    path("<slug:page>.html", views.flatpage, name="flatpage"),
    path("contact.html", views.flatpage, name="contact"),

    # API (products)
    path("api/categories/", views.api_categories, name="api_categories"),
    path("api/products/", views.api_products, name="api_products"),
    path("api/products/<int:pk>/", views.api_product_detail, name="api_product_detail"),
]
