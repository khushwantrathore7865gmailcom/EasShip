# Generated by Django 3.2.4 on 2021-11-25 22:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PatnerCompany', '0003_auto_20211124_1953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comp_profile',
            name='email',
        ),
    ]