from django.urls import path
from .views import *

urlpatterns = [
    path('send-otp/', SendEmailOTP.as_view()),
    path('verify-otp/', VerifyEmailOTP.as_view()),
    path('registration/', Registration.as_view()),
    path('face-verification/', FaceVerification.as_view()),
    path('profile-verification/', ProfileVerification.as_view()),
    path('login/', Login.as_view()),
    path('profile-create-data/', ProfileCreateData.as_view()),
]
