# MusShop/orders/views.py
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from catalog.models import Product
from .forms import OrderCreateForm
from .models import Order, OrderItem


def _safe_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _get_product_from_cart_item(key, item):
    """
    Определяем товар из элемента корзины:
    1) по product_id / id / pk
    2) если ключ корзины число — считаем его ID
    3) по slug (item['slug'] или ключ как slug)
    """
    # 1) явный ID
    if isinstance(item, dict):
        pid = (
            _safe_int(item.get("product_id"))
            or _safe_int(item.get("id"))
            or _safe_int(item.get("pk"))
        )
        if pid:
            try:
                return Product.objects.get(pk=pid)
            except Product.DoesNotExist:
                pass

    # 2) ключ как ID
    pid = _safe_int(key)
    if pid:
        try:
            return Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            pass

    # 3) slug
    slug = None
    if isinstance(item, dict):
        slug = item.get("slug")
    if not slug and isinstance(key, str):
        slug = key
    if slug:
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            pass

    return None


def order_create(request):
    """
    GET  -> показать форму оформления + содержимое корзины
    POST -> создать заказ и редирект на страницу успеха
    """
    cart = request.session.get("cart", {}) or {}

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if not form.is_valid():
            # Падаем обратно на форму (покажем ошибки)
            items, total = _preview_cart(cart)
            return render(request, "orders/create.html", {
                "form": form, "items": items, "total": total
            })

        order: Order = form.save(commit=False)
        if request.user.is_authenticated:
            order.user = request.user
        order.save()

        # Заполняем позиции заказа из корзины
        total_amount = Decimal("0")
        for key, item in (cart.items() if isinstance(cart, dict) else []):
            product = _get_product_from_cart_item(key, item)
            if not product:
                continue

            # qty
            raw_qty = 1
            if isinstance(item, dict):
                raw_qty = item.get("qty", item.get("quantity", item.get("count", 1)))
            qty = _safe_int(raw_qty, 1) or 1

            # price
            raw_price = item.get("price") if isinstance(item, dict) else None
            try:
                price = Decimal(str(raw_price)) if raw_price is not None else product.price
            except Exception:
                price = product.price

            OrderItem.objects.create(
                order=order,
                product=product,
                price=price,
                qty=qty,
            )
            total_amount += price * qty

        # сохраним итог
        order.total_amount = total_amount
        order.save(update_fields=["total_amount"])

        # очистим корзину
        request.session["cart"] = {}
        request.session.modified = True

        return redirect(reverse("orders:success", kwargs={"pk": order.id}))


    # GET: показать форму + превью корзины
    form = OrderCreateForm()
    items, total = _preview_cart(cart)
    return render(request, "orders/create.html", {"form": form, "items": items, "total": total})


def _preview_cart(cart_dict):
    """Собираем список позиций и сумму для показа на странице оформления."""
    items = []
    total = Decimal("0")
    for key, item in (cart_dict.items() if isinstance(cart_dict, dict) else []):
        product = _get_product_from_cart_item(key, item)
        if not product:
            continue
        raw_qty = item.get("qty", item.get("quantity", item.get("count", 1))) if isinstance(item, dict) else 1
        qty = _safe_int(raw_qty, 1) or 1
        raw_price = item.get("price") if isinstance(item, dict) else None
        try:
            price = Decimal(str(raw_price)) if raw_price is not None else product.price
        except Exception:
            price = product.price
        line_total = price * qty
        total += line_total
        items.append({"product": product, "qty": qty, "price": price, "line_total": line_total})
    return items, total


def order_success(request, pk: int):
    order = get_object_or_404(Order, pk=pk)
    return render(
        request,
        "orders/success.html",
        {"order": order, "order_total": order.total_value},
    )
