# Generated by Django 5.0 on 2023-12-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_rent_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
    ]
