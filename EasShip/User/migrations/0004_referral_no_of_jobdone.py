# Generated by Django 3.2.4 on 2022-01-03 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_commission_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='no_of_jobdone',
            field=models.IntegerField(null=True),
        ),
    ]