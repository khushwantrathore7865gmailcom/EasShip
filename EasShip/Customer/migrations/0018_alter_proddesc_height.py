# Generated by Django 3.2.4 on 2021-12-22 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0017_alter_customer_profile_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proddesc',
            name='height',
            field=models.FloatField(blank=True),
        ),
    ]
