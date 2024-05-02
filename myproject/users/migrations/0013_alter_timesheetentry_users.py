# Generated by Django 4.2.11 on 2024-04-30 09:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0012_rename_user_timesheetentry_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timesheetentry',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]