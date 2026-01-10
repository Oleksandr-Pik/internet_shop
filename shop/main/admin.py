from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from django.utils.html import format_html
from unfold.contrib.filters.admin import (
    MultipleChoicesDropdownFilter,
    MultipleRelatedDropdownFilter,
)

from main.models import Category, Product, Brand, SiteReview, ProductReview


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "image_preview"]
    search_fields = ['name']
    # readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" />', obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Прев'ю зображення"


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = [
        "name",
        "image_preview",
        "price",
        "discount",
        "in_stock",
        "brand",
        "category",
        "is_sells_better",
        "is_available",
    ]
    search_fields = ["name", "description"]
    list_filter = [
        ("brand", MultipleRelatedDropdownFilter),
        ("category", MultipleRelatedDropdownFilter),
        "price",
        "in_stock",
        "is_sells_better",
        "is_available",
    ]
    list_editable = ["is_sells_better", "in_stock", "is_available"]
    list_filter_submit = True
    ordering = ["-is_available", "name"]

    # def image_preview(self, obj):
    #     if obj.image:
    #         return format_html(
    #             f'<img src="{obj.image.url}" width="100" height="100"/>'
    #         )
    #     return "No Image"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" />', obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Прев'ю зображення"


@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    pass


@admin.register(SiteReview)
class SiteReviewAdmin(ModelAdmin):
    pass


@admin.register(ProductReview)
class ProductReviewAdmin(ModelAdmin):
    pass
