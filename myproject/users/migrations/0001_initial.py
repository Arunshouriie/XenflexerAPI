# Generated by Django 4.2.11 on 2024-04-18 09:19

from django.conf import settings
import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.FileField(upload_to='certificates/')),
                ('resume', models.FileField(upload_to='resumes/')),
                ('tax_document', models.FileField(upload_to='tax_documents/')),
                ('proof_of_identification', models.FileField(upload_to='proof_of_identifications/')),
                ('agreement', models.FileField(upload_to='agreements/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university', models.CharField(blank=True, max_length=100, null=True)),
                ('graduation', models.CharField(blank=True, max_length=100, null=True)),
                ('field_of_study', models.CharField(blank=True, max_length=100, null=True)),
                ('select_period', django.contrib.postgres.fields.ranges.DateRangeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('how_did_you_hear_about_us', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('working_on_project', models.BooleanField(default=True)),
                ('xenspire_is_the_employer', models.BooleanField(default=True)),
                ('do_you_want_xenspire_to_be', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='voluntary_disclosures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='workexpereience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('select_period', django.contrib.postgres.fields.ranges.DateRangeField()),
            ],
        ),
        migrations.CreateModel(
            name='TimesheetEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('hours_worked', models.DecimalField(decimal_places=2, max_digits=5)),
                ('project_description', models.TextField()),
                ('approval_status', models.CharField(choices=[('Approval', 'Approval'), ('Pending', 'Pending')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
