# Generated by Django 3.2.4 on 2021-09-18 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0004_shipjob_ship_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expired_ShipJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipjob')),
            ],
        ),
    ]
