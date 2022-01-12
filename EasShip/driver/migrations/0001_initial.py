# Generated by Django 3.2.4 on 2022-01-07 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PatnerCompany', '0029_comp_drivers_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='driverLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=30000)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.comp_drivers')),
            ],
        ),
    ]