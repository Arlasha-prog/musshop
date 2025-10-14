def cart(request):
    session_cart = request.session.get("cart", {})
    total_qty = sum(item.get("qty", 0) for item in session_cart.values())
    return {"cart_count": total_qty, "cart_items": session_cart}
