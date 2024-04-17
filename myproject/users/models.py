from django.db import models
from phone_field import PhoneField
# Create your models here.
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.db import models
from django.contrib.postgres.fields import DateRangeField
from django.contrib.auth.models import User

class TimesheetEntry(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    project_description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    APPROVAL_CHOICES = [
        ('Approval', 'Approval'),
        ('Pending', 'Pending')
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES)

class workexpereience(models.Model):
    job_title = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    select_period = DateRangeField()

class education(models.Model):
    university = models.CharField(max_length=100, blank=True, null=True)
    graduation = models.CharField(max_length=100, blank=True, null=True)
    field_of_study = models.CharField(max_length=100, blank=True, null=True)
    select_period = DateRangeField()

class DocumentUpload(models.Model):
    certificate = models.FileField(upload_to='certificates/')
    resume = models.FileField(upload_to='resumes/')
    tax_document = models.FileField(upload_to='tax_documents/')
    proof_of_identification = models.FileField(upload_to='proof_of_identifications/')
    agreement = models.FileField(upload_to='agreements/')
    uploaded_at = models.DateTimeField(auto_now_add=True)   

class voluntary_disclosures(models.Model):
    text = models.CharField(max_length=255)
    choices = [
        ('yes', 'yes'),
        ('no', 'no')
    ] 

class UserProfile(models.Model):
    mobile = PhoneField(blank=True, help_text='Contact phone number')
    how_did_you_hear_about_us = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    working_on_project = models.BooleanField(default=True)
    xenspire_is_the_employer = models.BooleanField(default=True)
    do_you_want_xenspire_to_be = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )