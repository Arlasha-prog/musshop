# MusShop/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка
    path("admin/", admin.site.urls),

    # Магазин (каталог, карточки, плоские страницы)
    path("", include("catalog.urls")),

    # Корзина
    path("cart/", include("cart.urls")),

    # Заказы (оформление)
     path("orders/", include(("orders.urls", "orders"), namespace="orders")),
    # Аккаунты (namespace)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
]

# Медиа-файлы (картинки товаров)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
