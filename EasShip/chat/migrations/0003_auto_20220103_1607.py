# Generated by Django 3.2.4 on 2022-01-03 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0019_alter_shipjob_job_description'),
        ('PatnerCompany', '0028_alter_comp_transport_transport_no_plate'),
        ('chat', '0002_message_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='userc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Customer.customer'),
        ),
        migrations.AddField(
            model_name='room',
            name='userp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp'),
        ),
    ]