from knox import views as knox_views
from .views import LoginAPI,LogoutView, RegisterAPI, UploadresumeRetrieveUpdateDestroy, uploadresumelistcreate, UserAPI, ChangePasswordView, TimesheetEntryListCreate, TimesheetEntryRetrieveUpdateDestroy, UserProfileView, WorkexperienceView, DocumentUploadListCreate, DocumentUploadRetrieveUpdateDestroy, voluntarydisclosureListCreate, voluntarydisclosureRetrieveUpdateDestroy, EducationView, JobOpportunityListCreateView, SalescontactView, ConatctUsView, UserTimesheetEntryView
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', UserProfileView, basename='user_profile'),
router.register(r'myexperience', WorkexperienceView, basename='work_experience'),
router.register(r'education', EducationView, basename='education')
router.register(r'contactsales', SalescontactView, basename = 'Salescontact')
router.register(r'contactus', ConatctUsView, basename = 'Conatctus')
router.register(r'user/timesheets', UserTimesheetEntryView, basename = 'usertimesheets')


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/user/', UserAPI.as_view(), name='user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('timesheets/', TimesheetEntryListCreate.as_view(), name='timesheet-list-create'),
    path('timesheets/<int:pk>/', TimesheetEntryRetrieveUpdateDestroy.as_view(), name='timesheet-detail'),
    path('', include(router.urls)),
    path('documents/', DocumentUploadListCreate.as_view(), name='document-upload-list-create'),
    path('documents/<int:pk>/', DocumentUploadRetrieveUpdateDestroy.as_view(), name='document-upload-detail'),
    path('upload/resume/', uploadresumelistcreate.as_view(), name='resume-upload-list-create'),
    path('upload/resume/<int:pk>/', UploadresumeRetrieveUpdateDestroy.as_view(), name='resume-upload-detail'),
    path('multiple_choice_questions/', voluntarydisclosureListCreate.as_view(), name='multiple-choice-question-list-create'),
    path('multiple_choice_questions/<int:pk>/', voluntarydisclosureRetrieveUpdateDestroy.as_view(), name='multiple-choice-question-detail'),
    path('interestsignup', JobOpportunityListCreateView.as_view(), name= 'interest-signup'),
]

# from django.urls import path
# from .views import TimesheetEntryListCreate, TimesheetEntryRetrieveUpdateDestroy

# urlpatterns = [
#     path('timesheets/', TimesheetEntryListCreate.as_view(), name='timesheet-list-create'),
#     path('timesheets/<int:pk>/', TimesheetEntryRetrieveUpdateDestroy.as_view(), name='timesheet-detail'),
# ]
