from django.urls import path
from orders.views import CreateOrderView

urlpatterns = [
   path("create-order/", CreateOrderView.as_view(), name="create_order"),
]
