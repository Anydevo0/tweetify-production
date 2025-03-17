from django.contrib import admin
from .models import Tweet, Profile


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
