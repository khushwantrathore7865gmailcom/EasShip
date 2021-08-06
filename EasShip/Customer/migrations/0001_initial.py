# Generated by Django 3.2.4 on 2021-07-25 11:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProdDesc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_box', models.IntegerField()),
                ('prod_in_box', models.IntegerField()),
                ('Weight_box', models.CharField(max_length=1024)),
                ('length', models.CharField(max_length=1024)),
                ('width', models.CharField(max_length=1024)),
                ('height', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='shipJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_description', models.CharField(max_length=1024)),
                ('picking_Address', models.CharField(max_length=1024)),
                ('droping_Address', models.CharField(max_length=1024)),
                ('cust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Customer_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Please enter valid phone number. Correct format is 91XXXXXXXX', regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, max_length=25)),
                ('company_type', models.CharField(blank=True, max_length=250)),
                ('company_name', models.CharField(blank=True, max_length=250)),
                ('company_logo', models.ImageField(blank=True, upload_to='')),
                ('cust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Customer_address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, verbose_name='Address line 2')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('state', models.CharField(max_length=1024, verbose_name='State')),
                ('country', models.CharField(max_length=1024, verbose_name='Country')),
                ('cust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customer')),
            ],
            options={
                'verbose_name': 'Customer Company Address',
                'verbose_name_plural': 'Customer Company Addresses',
            },
        ),
    ]