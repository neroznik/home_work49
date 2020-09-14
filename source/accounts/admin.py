from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['about', 'git_url', 'avatar']


class ProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


