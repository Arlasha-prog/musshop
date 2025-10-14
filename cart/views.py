from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart

@require_POST
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    qty = int(request.POST.get("qty", 1))
    replace = request.POST.get("replace") == "1"
    cart = Cart(request)
    cart.add(product, qty=qty, replace=replace)
    return redirect("cart_detail")

def cart_detail(request):
    cart = Cart(request)
    context = {
        "items": list(iter(cart)),
        "total_qty": cart.total_qty(),
        "total_price": cart.total_price(),
    }
    return render(request, "cart/detail.html", context)

@require_POST
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = Cart(request)
    cart.remove(product)
    return redirect("cart_detail")

@require_POST
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")
