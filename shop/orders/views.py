from django.shortcuts import render
from main.base_views import BaseView
from main.models import Product, Category, Brand
from cart.cart import Cart
from cart.models import CartItem


class CreateOrderView(BaseView):
    template_name = "orders/create_order.html"

    def _get_page_name(self, **kwargs):
        return "Замовлення"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            items = self.request.user.cart_items.all()
            total = sum(item.get_total_price() for item in items)
        else:
            cart = Cart(self.request)
            items = list(cart)
            total = cart.get_total_price()

        context["categorys"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        context["cart_items"] = items
        context["cart_total"] = total
        return context
