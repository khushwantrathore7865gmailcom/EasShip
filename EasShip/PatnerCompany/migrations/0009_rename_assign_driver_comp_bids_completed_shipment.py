# Generated by Django 3.2.4 on 2021-12-02 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PatnerCompany', '0008_comp_presentwork_ask_finalpay'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comp_bids',
            old_name='assign_driver',
            new_name='completed_shipment',
        ),
    ]
