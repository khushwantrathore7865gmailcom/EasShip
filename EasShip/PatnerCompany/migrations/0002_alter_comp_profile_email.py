# Generated by Django 3.2.9 on 2021-11-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PatnerCompany', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comp_profile',
            name='email',
            field=models.EmailField(blank=True, max_length=75),
        ),
    ]
