# Generated by Django 3.2.4 on 2021-09-25 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0006_shipment_related_question'),
        ('PatnerCompany', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comp_bids',
            name='is_disqualified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comp_bids',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comp_bids',
            name='is_shortlisted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Employer_candidate_jobanswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=1250)),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PatnerCompany.patnercomp')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.shipment_related_question')),
            ],
        ),
    ]
