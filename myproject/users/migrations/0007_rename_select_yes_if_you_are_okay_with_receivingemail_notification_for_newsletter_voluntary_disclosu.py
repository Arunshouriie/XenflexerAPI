# Generated by Django 4.2.11 on 2024-04-23 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_rename_please_select_yes_if_you_are_okay_with_receivingemail_notification_for_newsletter_voluntary_d'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voluntary_disclosures',
            old_name='select_YES_if_you_are_okay_with_receivingEmail_Notification_for_Newsletter',
            new_name='selectYESifyouareokayreceivingEmailNotificationforNewsletter',
        ),
        migrations.RenameField(
            model_name='voluntary_disclosures',
            old_name='select_YES_if_you_are_okay_with_receiving_updates_on_new_jobs_being_posted',
            new_name='selectYESifyouareokayreceivingupdatesonnewjobsbeingposted',
        ),
    ]
