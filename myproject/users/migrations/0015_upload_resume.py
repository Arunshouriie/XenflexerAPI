# Generated by Django 4.2.11 on 2024-05-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_jobopportunity_contract_type_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='upload_resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(upload_to='resume/')),
            ],
        ),
    ]