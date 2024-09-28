import stripe
from django.conf import settings


def create_stripe_product(course_title):
    # Создаем продукт в Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Product.create(
        name=course_title,
    )


def create_stripe_price(product_pk, price):
    # Создаем цену в Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.Price.create(
        product=product_pk,
        unit_amount=int(price * 100),
        currency="rub",
    )


def create_stripe_sessions_payment(price_id, success_url, cancel_url):
    # Создаем сессию в Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )


def retrieve_stripe_payment_status(stripe_session_id):
    # Получаем статус платежа в Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.retrieve(stripe_session_id)
        return session["payment_status"]
    except stripe.error.StripeError as e:
        raise ValueError(f"Ошибка при получении статуса платежа: {e}")
