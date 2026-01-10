from main.base_views import BaseView
from django.views import View
# from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from main.models import Product, Category, Brand
from cart.cart import Cart
from cart.models import CartItem


class CartDetailView(BaseView):
    template_name = "cart/cart_detail.html"

    def _get_page_name(self, **kwargs):
        return "Кошик"

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


class CartAddView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            item, created = CartItem.objects.get_or_create(
                user=request.user, product=product
            )
            if not created:
                item.quantity += 1
                item.save()
        else:
            cart = Cart(request)
            cart.add(product)

        return redirect(request.META.get("HTTP_REFERER", "catalog"))


class CartRemoveView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            CartItem.objects.filter(user=request.user, product=product).delete()
        else:
            cart = Cart(request)
            cart.remove(product)

        return redirect("cart_detail")


class CartUpdateView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        action = request.POST.get("action")

        if request.user.is_authenticated:
            item, _ = CartItem.objects.get_or_create(user=request.user, product=product)
            if action == "increase":
                item.quantity += 1
            elif action == "decrease":
                item.quantity -= 1

            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        else:
            cart = Cart(request)
            current_qty = cart.cart.get(str(product.id), {}).get("quantity", 0)

            if action == "increase":
                cart.update_quantity(product, current_qty + 1)
            elif action == "decrease":
                cart.update_quantity(product, current_qty - 1)

        return redirect("cart_detail")


class CartCountApiView(View):
    def get(self, request):
        if request.user.is_authenticated:
            count = sum(i.quantity for i in request.user.cart_items.all())
        else:
            cart = Cart(request)
            count = sum(item["quantity"] for item in cart.cart.values())
        return JsonResponse({"count": count})
