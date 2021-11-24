# Generated by Django 3.2.4 on 2021-11-19 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0009_shipjob_bid_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expired_shipjob',
            name='job_id',
        ),
        migrations.AddField(
            model_name='expired_shipjob',
            name='cust',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.customer'),
        ),
        migrations.AddField(
            model_name='expired_shipjob',
            name='droping_Address',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='expired_shipjob',
            name='job_description',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='expired_shipjob',
            name='picking_Address',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='expired_shipjob',
            name='ship_title',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]