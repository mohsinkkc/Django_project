# Generated by Django 5.0 on 2023-12-22 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_remove_cart_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction',
        ),
    ]
