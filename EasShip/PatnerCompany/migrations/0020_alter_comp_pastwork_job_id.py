# Generated by Django 3.2.4 on 2021-12-26 22:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0019_alter_shipjob_job_description'),
        ('PatnerCompany', '0019_comp_presentwork_request_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comp_pastwork',
            name='job_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.expired_shipjob'),
        ),
    ]