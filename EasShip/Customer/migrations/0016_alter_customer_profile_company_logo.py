# Generated by Django 3.2.4 on 2021-12-21 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0015_auto_20211220_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer_profile',
            name='company_logo',
            field=models.ImageField(blank=True, upload_to='customer_logo/'),
        ),
    ]