from django.contrib import admin
from .models import Salescontact, TimesheetEntry, JobOpportunity, ConatctUs

# Register your models here.
admin.site.register(Salescontact)
admin.site.register(TimesheetEntry)
admin.site.register(JobOpportunity)
admin.site.register(ConatctUs)
# admin.site.register()