# Generated by Django 3.2.4 on 2021-12-12 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PatnerCompany', '0013_orders_order_gone'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]
