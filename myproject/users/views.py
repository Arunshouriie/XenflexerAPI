from django.contrib.auth import login
from knox.views import LogoutView as KnoxLogoutView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from knox.views import LoginView as KnoxLoginView

from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from .models import JobOpportunity
from .serializers import JobOpportunitySerializer
from django.conf import settings
from .permissions import IsOwner
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from .models import TimesheetEntry, UserDetails,MyEducation, Timesheet, MyExperience, Documentsupload, UploadResume, VoluntaryDisclosures, Salescontact, ConatctUs
from .serializers import TimesheetEntrySerializer, TimesheetSerializer, UserProfileSerializer, uploadresumeSerializer, voluntarydisclosureSerializer, SalescontactSerializer, ConatctUsSerializer, UserTimesheetEntrySerializer, workexpereienceSerializer, educationSerializer, DocumentUploadSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'Please provide all required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        tokens = get_tokens_for_user(user)

        return Response({'message': 'User created successfully', 'tokens': tokens}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)

        # return Response({'tokens': tokens})
        return Response({
            'tokens': tokens,
            'user': {
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)

class TimesheetVIew(viewsets.ModelViewSet):
    queryset = Timesheet.objects.all()
    serializer_class = TimesheetSerializer
    permission_classes = [IsAuthenticated]
    
    

class TimesheetEntryListCreate(generics.ListCreateAPIView):
    queryset = TimesheetEntry.objects.all()
    serializer_class = TimesheetEntrySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class TimesheetEntryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TimesheetEntry.objects.all()
    serializer_class = TimesheetEntrySerializer
    permission_classes = [IsAuthenticated]

class TimesheetEntryListCreate(generics.ListCreateAPIView):
    serializer_class = TimesheetEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        approval_status = self.request.query_params.get('approval_status', None)
        if approval_status is not None:
            return TimesheetEntry.objects.filter(approval_status=approval_status)
        return TimesheetEntry.objects.all()

class UserTimesheetEntryView(viewsets.ModelViewSet):
   queryset = TimesheetEntry.objects.all()
   serializer_class = UserTimesheetEntrySerializer
   permission_classes = [IsAuthenticated]
   def get_queryset(self):
        # Only return timesheets created by the logged-in user
        return TimesheetEntry.objects.filter(users=self.request.user)

   def perform_create(self, serializer):
        # Save timesheet with the logged-in user as the owner
        serializer.save(users=self.request.user)
   def get_queryset(self):
        # Get all timesheets assigned to the logged-in user, sorted by date (latest first)
        return TimesheetEntry.objects.filter(users=self.request.user, is_active=True).order_by('-start_date')

# class LogoutView(KnoxLogoutView):
#     permission_classes = (permissions.IsAuthenticated,)

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    # obj = OnboardConfirmation(user_id)
    # authentication_classes = (TokenAuthentication,) 
    def get_object(self):
        # Retrieve the user profile of the authenticated user
        return UserDetails.objects.get(user=self.request.user)

    def get(self, request):
        # Get the user's profile using the get_object method
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        # Update the user's profile
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class OnboardConfirmationView():

class WorkexperienceView(viewsets.ModelViewSet):
    queryset = MyExperience.objects.all()
    serializer_class = workexpereienceSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    def create(self, request, *args, **kwargs):
        # Ensure incoming data is a list
        if not isinstance(request.data, list):
            return Response(
                {"non_field_errors": "Expected a list of objects."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate and create each item in the list
        serializer = self.get_serializer(data=request.data, many=True)  # Use many=True to handle lists
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def get_object(self):
        # Retrieve the user profile of the authenticated user
        return MyExperience.objects.get(user=self.request.user)

    def get(self, request):
        # Get the user's profile using the get_object method
        my_experience = self.get_object()
        serializer = workexpereienceSerializer(my_experience)
        return Response(serializer.data)

    def put(self, request):
        # Update the user's profile
        my_experience = self.get_object()
        serializer = workexpereienceSerializer(my_experience, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class EducationView(viewsets.ModelViewSet):
    queryset = MyEducation.objects.all()
    serializer_class = educationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    def create(self, request, *args, **kwargs):
        # Ensure incoming data is a list
        if not isinstance(request.data, list):
            return Response(
                {"non_field_errors": "Expected a list of objects."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate and create each item in the list
        serializer = self.get_serializer(data=request.data, many=True)  # Use many=True to handle lists
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def get_object(self):
        # Retrieve the user profile of the authenticated user
        return MyEducation.objects.get(user=self.request.user)

    def get(self, request):
        # Get the user's profile using the get_object method
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        # Update the user's profile
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentUploadListCreate(generics.ListCreateAPIView):
    queryset = Documentsupload.objects.all()
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        # Retrieve the user profile of the authenticated user
        return Documentsupload.objects.get(user=self.request.user)

    def get(self, request):
        # Get the user's profile using the get_object method
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    def put(self, request):
        # Update the user's profile
        user_profile = self.get_object()
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DocumentUploadRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Documentsupload.objects.all()
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated, IsOwner]
class UploadresumeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = UploadResume.objects.all()
    serializer_class = uploadresumeSerializer
    permission_classes = [IsAuthenticated, IsOwner]
class uploadresumelistcreate(generics.ListCreateAPIView):
    queryset = UploadResume.objects.all()
    serializer_class = uploadresumeSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class voluntarydisclosureListCreate(generics.ListCreateAPIView):
    queryset = VoluntaryDisclosures.objects.all()
    serializer_class = voluntarydisclosureSerializer
    permission_classes = [IsAuthenticated, IsOwner]

class voluntarydisclosureRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = VoluntaryDisclosures.objects.all()
    serializer_class = voluntarydisclosureSerializer
    permission_classes = [IsAuthenticated, IsOwner]

# Register API
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#         "user": UserSerializer(user, context=self.get_serializer_context()).data,
#         "token": AuthToken.objects.create(user)[1]
#         })

# Login API
# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, *args, **kwargs):
#         username = request.data.get('username')
#         password = request.data.get('password')
        
#         user = authenticate(request, username=username, password=password)
#         if not user:
#             return Response(
#                 {"error": "Invalid username or password"},
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
        
#         _, token = AuthToken.objects.create(user)
#         return Response({
#             "user_id": user.id,
#             "username": user.username,
#             "token": token,
#             "email": user.email
#         })

# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

ADMIN_EMAIL = "recruitment@xenspire.com"
class SalescontactView(viewsets.ModelViewSet):
    queryset = Salescontact.objects.all()
    serializer_class = SalescontactSerializer

    def perform_create(self, serializer):

       if serializer.is_valid():
        Salescontact = serializer.save()

        email_message = (
            f"Hello {Salescontact.first_name},\n\n"
            "Thank you for contacting the Xenflexer sales team! We appreciate you reaching out and letting us know your interest in our products.\n"
            "A member of our sales team will be in touch with you shortly to discuss your inquiry in more detail and answer any questions you may have. We aim to respond to all inquiries within one business day.\n\n"
            "In the meantime, you can explore our website at https://www.xenflexer.com to learn more about Xenflexer's offerings and how our solutions can benefit you.\n"
            "We look forward to connecting with you soon! \n\n"
            "Sincerely,\n"
            "Xenspire Group"
        )
        # Send acknowledgment email to the user
        send_mail(
            subject="Your Inquiry to Xenflexer Sales",
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[Salescontact.work_email],
        )

        admin_email_message = (
            "Hi team,\n\n"
            f"We have a new interest for {Salescontact.first_name} to join our Xenflexer program. Below are the details:\n\n"
            f"First Name: {Salescontact.first_name}\n"
            f"Last Name: {Salescontact.last_name}\n"
            f"Work Email: {Salescontact.work_email}\n"
            f"Message: {Salescontact.message}\n"
            "Kindly take cognizance of the inquiry and get in touch with the candidate.\n\n"
            "Regards,\n"
            "Xenspire Team"
        )
        # Send email to the admin
        send_mail(
            subject="Hire Inquiry Received",
            message=admin_email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[ADMIN_EMAIL],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
       else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    # permission_classes = (IsAuthenticated,)

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




ADMIN_EMAIL = "recruitment@xenspire.com"


class JobOpportunityListCreateView(generics.ListCreateAPIView):
    queryset = JobOpportunity.objects.all()
    serializer_class = JobOpportunitySerializer

    def perform_create(self, serializer):

       if serializer.is_valid():
        job_opportunity = serializer.save()

        email_message = (
            f"Hello {job_opportunity.full_name},\n\n"
            "Thank you for your interest in Xenflexer! We're thrilled that you took the time to fill out our interest form.\n"
            "We understand that you're looking for joining us in the Xenflexer program, and we're confident that it will be a valuable asset for you.\n\n"
            "In the coming days, you'll receive a call from us with more information about the program.\n"
            "In the meantime, feel free to explore our website at https://www.xenflexer.com to learn more about Xenflexer and how it can help you achieve your goals.\n\n"
            "We're also happy to answer any questions you may have. Please don't hesitate to reply to this email.\n\n"
            "Thanks again for your interest!\n"
            "Sincerely,\n"
            "Xenspire Group"
        )
        # Send acknowledgment email to the user
        send_mail(
            subject="Thanks for Your Interest in Xenspire! ",
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[job_opportunity.email],
        )

        admin_email_message = (
            "Hi team,\n\n"
            f"We have a new interest for {job_opportunity.full_name} to join our Xenflexer program. Below are the details:\n\n"
            f"Full Name: {job_opportunity.full_name}\n"
            f"Email: {job_opportunity.email}\n"
            f"Phone Number: {job_opportunity.phone_number}\n"
            f"Job Type: {job_opportunity.job_type}\n"
            f"Contract Type: {job_opportunity.contract_type}\n"
            f"Joining Preference: {job_opportunity.joining_preference}\n\n"
            "Kindly take cognizance of the inquiry and get in touch with the candidate.\n\n"
            "Regards,\n"
            "Xenspire Team"
        )
        # Send email to the admin
        send_mail(
            subject="Interest: Flexer Interest Received",
            message=admin_email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[ADMIN_EMAIL],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
       else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

ADMIN_EMAIL = "recruitment@xenspire.com"
class ConatctUsView(viewsets.ModelViewSet):
    queryset = ConatctUs.objects.all()
    serializer_class = ConatctUsSerializer

    def perform_create(self, serializer):

       if serializer.is_valid():
        ConatctUs = serializer.save()

        email_message = (
            f"Hello {ConatctUs.first_name},\n\n"
            "Thank you for contacting the Xenflexer sales team! We appreciate you reaching out and letting us know your interest in our products.\n"
            "A member of our sales team will be in touch with you shortly to discuss your inquiry in more detail and answer any questions you may have. We aim to respond to all inquiries within one business day.\n\n"
            "In the meantime, you can explore our website at https://www.xenflexer.com to learn more about Xenflexer's offerings and how our solutions can benefit you.\n"
            "We look forward to connecting with you soon! \n\n"
            "Sincerely,\n"
            "Xenspire Group"
        )
        # Send acknowledgment email to the user
        send_mail(
            subject="Thank you for contacting Xenflexer",
            message=email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[ConatctUs.email],
        )

        admin_email_message = (
            "Hi team,\n\n"
            f"We have a new interest for {ConatctUs.first_name} to join our Xenflexer program. Below are the details:\n\n"
            f"First Name: {ConatctUs.first_name}\n"
            f"Last Name: {ConatctUs.last_name}\n"
            f"Work Email: {ConatctUs.email}\n"
            f"Company Name: {ConatctUs.company_name} "
            f"Phone Number: {ConatctUs.phone_number}\n"
            f"Reason for Reaching Out: {ConatctUs.Reason_for_reaching_out}\n"
            "Kindly take cognizance of the inquiry and get in touch with the candidate.\n\n"
            "Regards,\n"
            "Xenspire Team"
        )
        # Send email to the admin
        send_mail(
            subject="Contact Inquiry Received",
            message=admin_email_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[ADMIN_EMAIL],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
       else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)