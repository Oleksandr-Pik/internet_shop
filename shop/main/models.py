import datetime
from django.db import models
from django.core.exceptions import ValidationError
from main.validators import rating_validator
from django.urls import reverse


def current_year():
    return datetime.date.today().year


def validate_year(value):
    year_now = datetime.date.today().year
    if value < 2000:
        raise ValidationError("Рік виробництва не може бути меншим за 2000.")
    if value > year_now:
        raise ValidationError(f"Рік виробництва не може бути більшим за {year_now}.")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис категорії")
    image = models.ImageField(
        upload_to="category/", blank=True, null=True, verbose_name="Фото"
    )

    @property
    def img(self):
        if self.image:
            return self.image.url
        else:
            return "/static/main/images/NO_IMAGE_BG.png"

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name} (id: {self.id})"

    def get_absolute_url(self):
        return reverse("category_view", args=[str(self.id)])


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва бренду")
    country = models.CharField(
        max_length=100, default="Не вказано", verbose_name="Країна походження"
    )
    # image = models.ImageField(
    #     upload_to="brand/", blank=True, null=True, verbose_name="Фото"
    # )

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренди"
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name} (id: {self.id})"

    def get_absolute_url(self):
        return reverse("brand_view", args=[str(self.id)])


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Назва товару")
    description = models.TextField(blank=True, verbose_name="Опис")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категорія",
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Бренд",
    )
    year_manufacture = models.PositiveIntegerField(
        default=current_year, validators=[validate_year], verbose_name="Рік виробництва"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    is_sells_better = models.BooleanField(
        default=False, verbose_name="Найчастіще купують"
    )
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="Фото"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступний")
    discount = models.DecimalField(
        default=0.00,
        max_digits=5,
        decimal_places=2,
        verbose_name="Знижка (%)",
    )
    in_stock = models.BooleanField(default=True, verbose_name="В наявності")
    # stock = models.PositiveIntegerField(default=0, verbose_name="Кількість на складі")
    # created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")
    # updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    @property
    def img(self):
        if self.image:
            return self.image.url
        else:
            return "/static/main/images/NOIMAGE.png"

    class Meta:
        ordering = ["name", "is_available"]
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.brand})"

    def get_absolute_url(self):
        return reverse("product_view", args=[str(self.id)])

    @property
    def sell_price(self):
        if self.discount > 0:
            discount_amount = round((self.discount / 100) * self.price)
            return self.price - discount_amount
        return self.price


class SiteReview(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(validators=[rating_validator])
    created_time = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_time"]
        verbose_name = "Відгуки про сайт"
        verbose_name_plural = "Відгуки про сайт"

    def __str__(self):
        return f"Відгук від {self.name}"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, validators=[rating_validator])
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Відгуки про товар"
        verbose_name_plural = "Відгуки про товари"

    def __str__(self):
        return f"Відгук від {self.name} для {self.product.name}"
