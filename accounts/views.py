from django.core.files.storage import default_storage
from django.conf import settings
from .models import State, Profession, Language, Hobby
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StateSerializer, ProfessionSerializer, LanguageSerializer, HobbySerializer
from .utils import detection_process, verify_profile
import uuid



class FaceVerification(APIView):
    def post(self, request):
        img = request.FILES.get('img')
        files = request.FILES.getlist('img')

        if not img:
            return Response({'error': 'img is required!'}, status=status.HTTP_404_NOT_FOUND)

        if len(files) > 1:
            return Response({'error': 'Multiple files found. Only one file is allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        result = detection_process(img)
        return result

class ProfileVerification(APIView):
    def post(self, request):
        img = request.FILES.get('img')
        video = request.FILES.get('video')

        if not img or not video:
            return Response({'error': 'img and video are required!'}, status=status.HTTP_404_NOT_FOUND)

        files = request.FILES.getlist('img') + request.FILES.getlist('video')
        if len(files) > 2:
            return Response({'error': 'Multiple files detected. Please upload only one file for img and one file for video.'}, status=status.HTTP_400_BAD_REQUEST)

        temps_folder = os.path.join(settings.BASE_DIR, 'temps')
        os.makedirs(temps_folder, exist_ok=True)
        
        try:
            file_extension = video.name.split('.')[-1]
            filename = f"{uuid.uuid4().hex}.{file_extension}"
            video_path = os.path.join(temps_folder, filename)
            default_storage.save(video_path, video)
        except:
            return Response({'error': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            profile_status = verify_profile(video_path, img)
            if profile_status == True:
                return Response({'msg': 'Profile verification completed.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Profile verification failed!'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'Something went wrong!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileCreateData(APIView):
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
