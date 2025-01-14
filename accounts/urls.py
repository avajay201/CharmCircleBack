from django.urls import path
from .views import *

urlpatterns = [
    path('face-verification/', FaceVerification.as_view()),
    path('profile-verification/', ProfileVerification.as_view()),
    path('profile-create-data/', ProfileCreateData.as_view()),
]
