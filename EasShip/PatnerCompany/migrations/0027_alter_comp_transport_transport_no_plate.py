# Generated by Django 3.2.4 on 2021-12-28 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PatnerCompany', '0026_alter_comp_transport_transport_no_plate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comp_transport',
            name='transport_no_plate',
            field=models.CharField(max_length=1),
        ),
    ]
