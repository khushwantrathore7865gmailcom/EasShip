# Generated by Django 3.2.4 on 2022-01-02 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='username',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
