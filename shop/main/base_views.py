from django.views.generic import TemplateView
from cart.cart import Cart
from cart.models import CartItem

class BaseView(TemplateView):

    def _get_page_name(self, **kwargs):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = self._get_page_name(**kwargs)
        context["cart_count"] = self.get_cart_count()

        return context

    def get_cart_count(self):
        request = self.request
        if request.user.is_authenticated:
            return sum(i.quantity for i in request.user.cart_items.all())
        else:
            cart = Cart(request)
            return sum(item["quantity"] for item in cart.cart.values())
