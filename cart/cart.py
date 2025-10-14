from decimal import Decimal
from django.conf import settings
from catalog.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, qty=1, override_qty=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"qty": 0, "price": str(product.price)}
        if override_qty:
            self.cart[product_id]["qty"] = qty
        else:
            self.cart[product_id]["qty"] += qty
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item["product"] = product
            cart_item["price"] = Decimal(cart_item["price"])
            cart_item["total_price"] = cart_item["price"] * cart_item["qty"]
            yield cart_item

    def __len__(self):
        return sum(item["qty"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["qty"] for item in self.cart.values()
        )

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()
# cart/cart.py
from decimal import Decimal
from django.conf import settings
from catalog.models import Product

CART_SESSION_ID = getattr(settings, "CART_SESSION_ID", "cart")

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if cart is None:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product: Product, qty: int = 1, replace: bool = False):
        pid = str(product.id)
        if pid not in self.cart:
            # храним цену как строку, чтобы сериализовалась в сессию
            self.cart[pid] = {"qty": 0, "price": str(product.price)}
        if replace:
            self.cart[pid]["qty"] = max(0, int(qty))
        else:
            self.cart[pid]["qty"] = int(self.cart[pid]["qty"]) + int(qty)
        # если кол-во стало 0 — удаляем позицию
        if self.cart[pid]["qty"] <= 0:
            del self.cart[pid]
        self.save()

    def remove(self, product: Product):
        pid = str(product.id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            data = self.cart[str(product.id)]
            price = Decimal(str(data["price"]))
            qty = int(data["qty"])
            yield {
                "product": product,
                "price": price,
                "quantity": qty,
                "total_price": price * qty,
            }

    def total_qty(self):
        return sum(int(item["qty"]) for item in self.cart.values())

    def total_price(self):
        return sum(Decimal(str(i["price"])) * int(i["qty"]) for i in self.cart.values())
