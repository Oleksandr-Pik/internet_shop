from django.urls import path
from .views import (
    CartDetailView,
    CartAddView,
    CartRemoveView,
    CartUpdateView,
    CartCountApiView,
)

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:product_id>/", CartAddView.as_view(), name="cart_add"),
    path("remove/<int:product_id>/", CartRemoveView.as_view(), name="cart_remove"),
    path("update/<int:product_id>/", CartUpdateView.as_view(), name="cart_update"),
    path("count/", CartCountApiView.as_view(), name="cart_count_api"),
]
