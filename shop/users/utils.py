from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from cart.cart import Cart
from cart.models import CartItem
from main.models import Product


def merge_cart_to_user(request):
    """
    Переносить товари з сесійного кошика у CartItem для авторизованого користувача.
    """
    if not request.user.is_authenticated:
        return

    cart = Cart(request)
    for product_id_str, item in cart.cart.items():
        product_id = int(product_id_str)
        product = Product.objects.filter(id=product_id).first()
        if not product:
            continue

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:
            cart_item.quantity += item["quantity"]
        else:
            cart_item.quantity = item["quantity"]
        cart_item.save()

    # Очищуємо сесію
    cart.clear()


def send_activation_email(email: str, activation_link: str) -> None:
    subject = "Активація вашого облікового запису"
    from_email = settings.EMAIL_HOST_USER
    html_message = render_to_string(
        "users/email_confirmation.html",
        {"activation_link": activation_link},
    )

    send_mail(
        subject=subject,
        message="",
        from_email=from_email,
        recipient_list=[email],
        html_message=html_message,
    )
