# Generated by Django 3.2.4 on 2021-09-25 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0006_shipment_related_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipjob',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]