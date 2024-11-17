from django.contrib import admin
from .models import UserLink, UserProfile
# Register your models here.

@admin.register(UserLink)
class UserLinkAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id',)