from .models import State, Profession, Language, Hobby
from rest_framework.serializers import ModelSerializer


class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class ProfessionSerializer(ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'

class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class HobbySerializer(ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'
