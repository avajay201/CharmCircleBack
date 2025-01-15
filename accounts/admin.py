from django.contrib import admin
from .models import OTP, State, Profession, Language, Hobby, Profile, ProfilePicture


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    search_fields = ['email']
    list_filter = ['email']
    readonly_fields = ['created_at']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_filter = ['user__username']

@admin.register(ProfilePicture)
class ProfilePictureAdmin(admin.ModelAdmin):
    search_fields = ['profile__user__username']
    list_filter = ['profile__user__username']
