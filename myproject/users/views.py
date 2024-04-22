from django.contrib.auth import login

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.views import APIView
from .models import TimesheetEntry, UserProfile, DocumentUpload, voluntary_disclosures, workexpereience, education, InterestSignup, Salescontact
from .serializers import TimesheetEntrySerializer, UserProfileSerializer, DocumentUploadSerializer, voluntarydisclosureSerializer, workexpereienceSerializer, educationSerializer, InterestSignupSerializer, SalescontactSerializer

class TimesheetEntryListCreate(generics.ListCreateAPIView):
    queryset = TimesheetEntry.objects.all()
    serializer_class = TimesheetEntrySerializer

class TimesheetEntryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimesheetEntry.objects.all()
    serializer_class = TimesheetEntrySerializer

class TimesheetEntryListCreate(generics.ListCreateAPIView):
    serializer_class = TimesheetEntrySerializer

    def get_queryset(self):
        approval_status = self.request.query_params.get('approval_status', None)
        if approval_status is not None:
            return TimesheetEntry.objects.filter(approval_status=approval_status)
        return TimesheetEntry.objects.all()

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class WorkexperienceView(viewsets.ModelViewSet):
    queryset = workexpereience.objects.all()
    serializer_class = workexpereienceSerializer

class EducationView(viewsets.ModelViewSet):
    queryset = education.objects.all()
    serializer_class = educationSerializer

class DocumentUploadListCreate(generics.ListCreateAPIView):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer

class DocumentUploadRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer

class voluntarydisclosureListCreate(generics.ListCreateAPIView):
    queryset = voluntary_disclosures.objects.all()
    serializer_class = voluntarydisclosureSerializer

class voluntarydisclosureRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = voluntary_disclosures.objects.all()
    serializer_class = voluntarydisclosureSerializer

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# job_opportunities/views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import InterestSignup
from .serializers import InterestSignupSerializer
from django.core.mail import send_mail

class InterestsignupCreateView(generics.CreateAPIView):
    queryset = InterestSignup.objects.all()
    serializer_class = InterestSignupSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Send acknowledgement email
        user_email = request.data.get('email')
        admin_email = 'recruitment@xenspire.com'  # Replace with your admin email
        send_mail(
            'Acknowledgement Email',
            'Thank you for submitting your information!',
            'your_email@example.com',
            [user_email, admin_email],
            fail_silently=False,
        )
        return response
    
    def get(self, request, *args, **kwargs):
        user_info = InterestSignup.objects.all()
        serializer = InterestSignupSerializer(user_info, many=True)
        return Response(serializer.data)

class SalescontactView(viewsets.ModelViewSet):
    queryset = Salescontact.objects.all()
    serializer_class = SalescontactSerializer


from rest_framework import generics, permissions

# Change Password
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated   

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)