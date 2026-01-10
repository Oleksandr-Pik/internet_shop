from decimal import Decimal
from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.sell_price)}
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def update_quantity(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity
            if self.cart[product_id]["quantity"] <= 0:
                del self.cart[product_id]
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            price = Decimal(item["price"])
            total_price = price * item["quantity"]
            yield {
                "product": product,
                "quantity": item["quantity"],
                "total_price": total_price,
                "get_total_price": total_price,
            }

    def clear(self):
        self.session["cart"] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        """Повертає загальну суму кошика (для гостей)."""
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
