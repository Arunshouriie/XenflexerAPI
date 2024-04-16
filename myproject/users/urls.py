from knox import views as knox_views
from .views import LoginAPI, RegisterAPI, UserAPI, ChangePasswordView, TimesheetEntryListCreate, TimesheetEntryRetrieveUpdateDestroy, UserProfileView
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profile', UserProfileView, basename='user_profile')

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
]

# from django.urls import path
# from .views import TimesheetEntryListCreate, TimesheetEntryRetrieveUpdateDestroy

# urlpatterns = [
#     path('timesheets/', TimesheetEntryListCreate.as_view(), name='timesheet-list-create'),
#     path('timesheets/<int:pk>/', TimesheetEntryRetrieveUpdateDestroy.as_view(), name='timesheet-detail'),
# ]
