# Generated by Django 3.2.4 on 2021-08-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0003_proddesc_shipment'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipjob',
            name='ship_title',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]