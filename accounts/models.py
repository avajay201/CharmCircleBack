from django.db import models
from django.contrib.auth.models import User


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    otp_sent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.otp} from {self.email}'

class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profession(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Hobby(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class GenderChoices(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'
    OTHER = 'Other', 'Other'

class Profile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GenderChoices.choices, max_length=6, null=True) # need to remove null
    dob = models.DateField()
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True)
    bio = models.TextField(null=True)
    state = models.ForeignKey(State, null=True, on_delete=models.SET_NULL)
    profession = models.ForeignKey(Profession, null=True, on_delete=models.SET_NULL)
    languages = models.ManyToManyField(Language)
    hobbies = models.ManyToManyField(Hobby)
    suggest_me_by_location = models.BooleanField(default=False)
    suggest_others_by_location = models.BooleanField(default=False)
    profile_verified = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class ProfilePicture(models.Model):
    profile = models.ForeignKey(Profile, related_name='additional_pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/extra/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.uploaded_at}"
