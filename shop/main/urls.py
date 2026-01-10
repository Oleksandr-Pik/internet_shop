from django.urls import path
from main.views import (
    HomePageView,
    CatalogView,
    BrandView,
    CategoryView,
    AboutView,
    ProductView,
)


urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("about/", AboutView.as_view(), name="about"),
    path("brand/<int:brand_id>/", BrandView.as_view(), name="brand_view"),
    path("category/<int:category_id>/", CategoryView.as_view(), name="category_view"),
    path("product/<int:product_id>/", ProductView.as_view(),name="product_view"),
]
