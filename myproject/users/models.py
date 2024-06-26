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

class Timesheet(models.Model):
    name = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    users = models.ManyToManyField(User)
    is_active = models.BooleanField(default=False)
class TimesheetEntry(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    users = models.ManyToManyField(User)
    APPROVAL_CHOICES = [
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    ]
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES)
    is_active = models.BooleanField(default=False)

class MyExperience(models.Model):
    userId = models.IntegerField(blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    currentCompany = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    my_exp = models.BooleanField(default=False)
    

class MyEducation(models.Model):
    userId = models.IntegerField(blank=True, null=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    graduation = models.CharField(max_length=100, blank=True, null=True)
    fieldOfStudy = models.CharField(max_length=100, blank=True, null=True)
    startDate = models.DateField()
    endDate = models.DateField()
    my_edu = models.BooleanField(default=False)

class Documentsupload(models.Model):
    userId = models.IntegerField(blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/')
    resume = models.FileField(upload_to='resumes/')
    tax = models.FileField(upload_to='tax_documents/')
    proof = models.FileField(upload_to='proof_of_identifications/')
    agreement = models.FileField(upload_to='agreements/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    docs = models.BooleanField(default=False)


class UploadResume(models.Model):
    userId = models.IntegerField(blank=True, null=True)
    upload = models.FileField(upload_to='resume/')

class VoluntaryDisclosures(models.Model):
    UPDATE_CHOICES = [
        ('yes', 'yes'),
        ('no', 'no')
    ] 
    selectYESifyouareokayreceivingupdatesonnewjobsbeingposted = models.CharField(max_length=255, choices = UPDATE_CHOICES, null = True)
    RECIEVE_CHOICES = [
        ('yes', 'yes'),
        ('no', 'no')
    ] 
    selectYESifyouareokayreceivingEmailNotificationforNewsletter = models.CharField(max_length=255, choices = UPDATE_CHOICES, null = True)
    disclosure = models.BooleanField(default=False)

class UserDetails(models.Model):
    userId = models.IntegerField(blank=True, null=True)
    mobile = PhoneField(blank=True, help_text='Contact phone number')
    how_did_you_hear_about_us = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    working_on_project = models.BooleanField(default=True)
    xenspire_is_the_employer = models.BooleanField(default=True)
    do_you_want_xenspire_to_be = models.BooleanField(default=True)
#     school = models.CharField(max_length=100, blank=True, null=True)
#     graduation = models.CharField(max_length=100, blank=True, null=True)
#     fieldOfStudy = models.CharField(max_length=100, blank=True, null=True)
#     startDate = models.DateField()
#     endDate = models.DateField()
#     upload = models.FileField(upload_to='resume/')
#     job_title = models.CharField(max_length=100, blank=True, null=True)
#     company_name = models.CharField(max_length=100, blank=True, null=True)
#     location = models.CharField(max_length=100, blank=True, null=True)
#     currentCompany = models.BooleanField(default=False)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     certificate = models.FileField(upload_to='certificates/')
#     resume = models.FileField(upload_to='resumes/')
#     tax = models.FileField(upload_to='tax_documents/')
#     proof = models.FileField(upload_to='proof_of_identifications/')
#     agreement = models.FileField(upload_to='agreements/')
#     uploaded_at = models.DateTimeField(auto_now_add=True) 
#     # userId = models.IntegerField(blank=True, null=True)
#     UPDATE_CHOICES = [
#         ('yes', 'yes'),
#         ('no', 'no')
#     ] 
#     selectYESifyouareokayreceivingupdatesonnewjobsbeingposted = models.CharField(max_length=255, choices = UPDATE_CHOICES, null = True)
#     RECIEVE_CHOICES = [
#         ('yes', 'yes'),
#         ('no', 'no')
#     ] 
#     selectYESifyouareokayreceivingEmailNotificationforNewsletter = models.CharField(max_length=255, choices = UPDATE_CHOICES, null = True)
    my_info = models.BooleanField(default=False)
#     my_exp = models.BooleanField(default=False)
#     my_edu = models.BooleanField(default=False)
#     docs = models.BooleanField(default=False)
#     disclosure = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# class Onboardconfirmation(models.Model):
#     userId = models.IntegerField(blank=True, null=True)
#     my_info = models.BooleanField(default=False)
#     my_exp = models.BooleanField(default=False)
#     my_edu = models.BooleanField(default=False)
#     docs = models.BooleanField(default=False)
#     disclosure = models.BooleanField(default=False)

class JobOpportunity(models.Model):
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField(max_length=70,blank=True,unique=True, null = True)
    # INTEREST_CHOICES =  [
    #     ('Non-Entry-Level Positions', 'Non-Entry-Level Positions'),
    #     ('Entry-Level Positions', 'Entry-Level Positions')
    # ] 
    job_type = models.CharField(max_length=255)
    # JOB_CHOICES =  [
    #     ('Permanent Positions', 'Permanent Positions'),
    #     ('Contract Positions', 'Contract Positions')
    # ] 
    contract_type = models.CharField(max_length=255)

    # CONTRACT_CHOICES = [
    #     ('Join with a new contract found by XenFlexer', 'Join with a new contract found by XenFlexer'),
    #     ('Join XenFlexer with a new contract I secure independently', 'Join XenFlexer with a new contract I secure independently'),
    #     ('Join XenFlexer with my current ongoing project', 'Join XenFlexer with my current ongoing project')
    # ]
    joining_preference =  models.CharField(max_length=255, help_text='Applicable only if you selected "Contract Positions" above.')

    def __str__(self):
        return f"{self.full_name}"

class Salescontact(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    work_email = models.EmailField(max_length=70,blank=True,unique=True, null = True)
    message = models.CharField(max_length=100, blank=True, null=True)

class ConatctUs(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=70,blank=True, null = True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    Reason_for_reaching_out = models.CharField(max_length=100, blank=True, null=True)


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