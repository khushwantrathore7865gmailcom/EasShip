# Generated by Django 3.2.4 on 2021-10-01 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0008_shipjob_created_on'),
        ('PatnerCompany', '0003_rename_employer_candidate_jobanswer_shipjob_jobanswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='shipJob_Saved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipjob')),
            ],
        ),
    ]
