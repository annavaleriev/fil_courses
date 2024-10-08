# Generated by Django 5.1 on 2024-09-26 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_usersubscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="stripe_payment_url",
            field=models.URLField(
                blank=True,
                help_text="URL оплаты Stripe",
                null=True,
                verbose_name="URL оплаты Stripe",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="stripe_session_id",
            field=models.CharField(
                blank=True,
                help_text="ID сессии Stripe",
                max_length=150,
                null=True,
                verbose_name="ID сессии Stripe",
            ),
        ),
    ]
