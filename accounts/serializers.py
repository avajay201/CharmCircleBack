from .models import User, Profile, ProfilePicture, State, Profession, Language, Hobby
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(write_only=True)
    dob = serializers.DateField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'gender', 'dob']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        gender = validated_data.pop('gender')
        dob = validated_data.pop('dob')
        user = User.objects.create_user(**validated_data)
        print(user, '|', gender, '|', dob)
        Profile.objects.create(user=user, gender=gender, dob=dob)
        return user

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = '__all__'
