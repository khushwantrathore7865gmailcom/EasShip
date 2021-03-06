# Generated by Django 3.2.4 on 2021-10-19 10:31

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Customer', '0008_shipjob_created_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='comp_Bids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Bid_amount', models.CharField(max_length=1024)),
                ('complete_in', models.IntegerField()),
                ('bid_on', models.DateTimeField(auto_now_add=True)),
                ('is_shortlisted', models.BooleanField(default=False)),
                ('is_disqualified', models.BooleanField(default=False)),
                ('is_selected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='comp_drivers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('phone', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Please enter valid phone number. Correct format is 91XXXXXXXX', regex='^\\+?1?\\d{9,15}$')])),
            ],
        ),
        migrations.CreateModel(
            name='patnerComp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='shipJob_Saved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipjob')),
            ],
        ),
        migrations.CreateModel(
            name='shipJob_jobanswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1250)),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipment_related_question')),
            ],
        ),
        migrations.CreateModel(
            name='comp_Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_transport', models.CharField(max_length=1024)),
                ('transport_no_plate', models.CharField(max_length=10)),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
            ],
        ),
        migrations.CreateModel(
            name='Comp_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator(message='Please enter valid phone number. Correct format is 91XXXXXXXX', regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, max_length=25)),
                ('company_type', models.CharField(blank=True, max_length=250)),
                ('company_name', models.CharField(blank=True, max_length=250)),
                ('company_logo', models.ImageField(blank=True, upload_to='')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
            ],
        ),
        migrations.CreateModel(
            name='comp_PresentWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_status', models.CharField(max_length=1024)),
                ('payment_Done', models.CharField(max_length=1024)),
                ('Payment_complete', models.BooleanField(default=False)),
                ('Total_payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.comp_bids')),
                ('co_driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codrivers', to='PatnerCompany.comp_drivers')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drivers', to='PatnerCompany.comp_drivers')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipjob')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transports', to='PatnerCompany.comp_transport')),
            ],
        ),
        migrations.CreateModel(
            name='comp_PastWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rating', models.CharField(max_length=1024)),
                ('delivered_on', models.DateTimeField(auto_now_add=True)),
                ('co_driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codriver', to='PatnerCompany.comp_drivers')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver', to='PatnerCompany.comp_drivers')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipjob')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport', to='PatnerCompany.comp_transport')),
            ],
        ),
        migrations.AddField(
            model_name='comp_drivers',
            name='comp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp'),
        ),
        migrations.AddField(
            model_name='comp_bids',
            name='comp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp'),
        ),
        migrations.AddField(
            model_name='comp_bids',
            name='job_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipjob'),
        ),
        migrations.CreateModel(
            name='Comp_address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.CharField(max_length=1024, verbose_name='Address line 1')),
                ('address2', models.CharField(max_length=1024, verbose_name='Address line 2')),
                ('zip_code', models.CharField(max_length=12, verbose_name='ZIP / Postal code')),
                ('city', models.CharField(max_length=1024, verbose_name='City')),
                ('state', models.CharField(max_length=1024, verbose_name='State')),
                ('country', models.CharField(max_length=1024, verbose_name='Country')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
            ],
            options={
                'verbose_name': 'Shipping Company Address',
                'verbose_name_plural': 'Shipping Company Addresses',
            },
        ),
    ]
