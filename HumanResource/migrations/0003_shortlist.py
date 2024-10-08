# Generated by Django 5.1.1 on 2024-10-01 04:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HumanResource', '0002_applicant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shortlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('summary', models.CharField(max_length=1000)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shortlisted_jobs', to='HumanResource.applicant')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shortlist', to='HumanResource.job')),
            ],
        ),
    ]
