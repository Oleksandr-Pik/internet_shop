from cart.cart import Cart


def cart_item_count(request):
    if request.user.is_authenticated:
        return {"cart_count": request.user.cart_items.count()}
    else:
        cart = Cart(request)
        count = sum(item["quantity"] for item in cart.cart.values())
        return {"cart_count": count}
