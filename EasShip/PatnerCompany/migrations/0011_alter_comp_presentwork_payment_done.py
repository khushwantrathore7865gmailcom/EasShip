# Generated by Django 3.2.4 on 2021-12-10 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PatnerCompany', '0010_auto_20211210_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comp_presentwork',
            name='payment_Done',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]