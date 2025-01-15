from datetime import timedelta
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import OTP, State, Profession, Language, Hobby
import os
import random
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, StateSerializer, ProfessionSerializer, LanguageSerializer, HobbySerializer
from .utils import detection_process, verify_profile
import uuid


class SendEmailOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                return Response({'error': 'A user already exists with this username'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.filter(email=email).first()
                if user:
                    return Response({'error': 'A user already exists with this email'}, status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response({'error': 'Email address is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_obj, created = OTP.objects.get_or_create(email=email)
            current_time = now()

            if not created and (current_time - otp_obj.created_at) >= timedelta(days=1):
                otp_obj.otp_sent = 0

            if not created and otp_obj.otp_sent >= 5:
                return Response({'error': 'You have exceeded the limit. Please try again after 24 hours.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            if not created and otp_obj.created_at > current_time - timedelta(minutes=1):
                return Response({'error': 'OTP already sent. Please wait a minute before requesting again.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

            otp = str(random.randint(100000, 999999))
            otp_obj.otp = otp
            otp_obj.otp_sent += 1
            send_mail('Charm Circle Verification OTP', f'Your OTP is {otp}', settings.EMAIL_HOST_USER, [email])
            otp_obj.save()
            return Response({'message': 'OTP sent successfully. Please check your email.'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyEmailOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        if not email or not otp:
            return Response({'error': 'Email and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            otp_obj = OTP.objects.get(email=email, otp=otp)
            if (now() - otp_obj.created_at) >= timedelta(minutes=1):
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

            otp_obj.delete()
            return Response({'message': 'OTP verified.'}, status=status.HTTP_200_OK)
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class Registration(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FaceVerification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        img = request.FILES.get('img')
        files = request.FILES.getlist('img')

        if not img:
            return Response({'error': 'img is required'}, status=status.HTTP_400_BAD_REQUEST)

        if len(files) > 1:
            return Response({'error': 'Multiple files found. Only one file is allowed'}, status=status.HTTP_400_BAD_REQUEST)

        result = detection_process(img)
        return result

class ProfileVerification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        img = request.FILES.get('img')
        video = request.FILES.get('video')

        if not img or not video:
            return Response({'error': 'img and video are required'}, status=status.HTTP_400_BAD_REQUEST)

        files = request.FILES.getlist('img') + request.FILES.getlist('video')
        if len(files) > 2:
            return Response({'error': 'Multiple files detected. Please upload only one file for img and one file for video'}, status=status.HTTP_400_BAD_REQUEST)

        temps_folder = os.path.join(settings.BASE_DIR, 'temps')
        os.makedirs(temps_folder, exist_ok=True)
        
        try:
            file_extension = video.name.split('.')[-1]
            filename = f"{uuid.uuid4().hex}.{file_extension}"
            video_path = os.path.join(temps_folder, filename)
            default_storage.save(video_path, video)
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            profile_status = verify_profile(video_path, img)
            if profile_status == True:
                return Response({'msg': 'Profile verification completed'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Profile verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileCreateData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        states = State.objects.all()
        professions = Profession.objects.all()
        languages = Language.objects.all()
        hobbies = Hobby.objects.all()
        
        state_serializer = StateSerializer(states, many=True)
        profession_serializer = ProfessionSerializer(professions, many=True)
        language_serializer = LanguageSerializer(languages, many=True)
        hobbie_serializer = HobbySerializer(hobbies, many=True)

        data = {
            'states': state_serializer.data,
            'professions': profession_serializer.data,
            'languages': language_serializer.data,
            'hobbies': hobbie_serializer.data,
        }
        
        return Response(data, status=status.HTTP_200_OK)
