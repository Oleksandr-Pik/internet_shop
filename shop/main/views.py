from main.base_views import BaseView
from main.models import Category, Product, Brand, SiteReview, ProductReview
from main.forms import SiteReviewForm, ProductReviewForm
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q


class PerformSearchMixin:

    def filter_products_by_search(self, request: HttpRequest, qs):
        search_query = request.GET.get("search", "").strip()
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        if search_query:
            qs = qs.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        return qs


class HomePageView(BaseView):
    template_name = "main/index.html"

    def _get_page_name(self, **kwargs):
        return "Головна"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sells_better_products"] = Product.objects.filter(is_sells_better=True, is_available=True)
        context["categorys"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        context["site_reviews"] = SiteReview.objects.all()
        form = kwargs.get("form")
        if not form:
            context["form"] = SiteReviewForm()
        else:
            context["form"] = form
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        form = SiteReviewForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            kwargs["form"] = form

        return self.render_to_response(self.get_context_data(**kwargs))


class CatalogView(BaseView, PerformSearchMixin):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        return "Каталог"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_available=True)
        context["products"] = self.filter_products_by_search(self.request, products)
        context["categorys"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        return context


class BrandView(BaseView, PerformSearchMixin):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        brand_name = kwargs.get("brand_name")
        return f"Товари бренду: {brand_name}"

    def get_context_data(self, **kwargs):
        brand_id = kwargs.get("brand_id")
        brand = Brand.objects.get(id=brand_id)
        kwargs["brand_name"] = brand.name

        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(brand_id=brand_id, is_available=True)
        context["products"] = self.filter_products_by_search(self.request, products)
        context["categorys"] = Category.objects.all()
        context["brands"] = Brand.objects.all()

        return context


class CategoryView(BaseView, PerformSearchMixin):
    template_name = "main/catalog.html"

    def _get_page_name(self, **kwargs):
        category_name = kwargs.get("category_name")
        return f"Товари з категорії: {category_name}"

    def get_context_data(self, **kwargs):
        category_id = kwargs.get("category_id")
        category = Category.objects.get(id=category_id)
        kwargs["category_name"] = category.name

        context = super().get_context_data(**kwargs)
        # context["products"] = Product.objects.filter(category_id=category_id)
        products = category.products.filter(is_available=True)
        context["products"] = self.filter_products_by_search(self.request, products)
        context["categorys"] = Category.objects.all()
        context["brands"] = Brand.objects.all()

        return context


class AboutView(HomePageView):
    template_name = "main/about.html"

    def _get_page_name(self, **kwargs):
        return "Про нас"


class ProductView(BaseView):
    template_name = "main/product.html"

    def _get_page_name(self, **kwargs):
        product_id = kwargs.get("product_id")
        product = Product.objects.get(id=product_id)
        product_name = product.name
        return f"{product_name}"

    def get_context_data(self, **kwargs):
        product_id = kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        context = super().get_context_data(**kwargs)
        context["product"] = product
        context["categorys"] = Category.objects.all()
        context["brands"] = Brand.objects.all()
        context["related_products"] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        context["reviews"] = ProductReview.objects.filter(product=product)

        form = kwargs.get("form")
        if not form:
            context["form"] = ProductReviewForm()
        else:
            context["form"] = form

        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            messages.success(request, "Ваш відгук успішно додано!")
            return redirect(
                reverse(
                    "product_view",
                    kwargs={"product_id": product.id},
                )
            )
        else:
            kwargs["form"] = form
            messages.error(request, "Будь ласка, виправте помилки у формі.")

        return self.render_to_response(self.get_context_data(**kwargs))
