from rest_framework import generics, permissions
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TimesheetEntry, UserProfile, myeducation, DocumentsUpload, upload_resume, myexperience, voluntary_disclosures, JobOpportunity, Salescontact, ConatctUs

class TimesheetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = '__all__'

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        timesheet = TimesheetEntry.objects.create(**validated_data)

        # Use set() to assign users to the timesheet
        timesheet.users.set(users_data)

        return timesheet

    def update(self, instance, validated_data):
        users_data = validated_data.pop('users', None)

        if users_data is not None:
            # Use set() to update the users for the timesheet
            instance.users.set(users_data)

        return super().update(instance, validated_data)

class educationSerializer(serializers.ModelSerializer):
    class Meta:
        model = myeducation
        fields = '__all__'
class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentsUpload
        fields = '__all__'

class UserTimesheetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = ['id','start_date', 'end_date', 'hours_worked', 'is_active']

class workexpereienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = myexperience
        fields = '__all__'

class uploadresumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = upload_resume
        fields = '__all__'


class voluntarydisclosureSerializer(serializers.ModelSerializer):
    class Meta:
        model = voluntary_disclosures
        fields = '__all__'

class ConatctUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConatctUs
        fields = '__all__'
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class JobOpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOpportunity
        fields = '__all__'

class SalescontactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salescontact
        fields = '__all__'
# Change Password
from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)