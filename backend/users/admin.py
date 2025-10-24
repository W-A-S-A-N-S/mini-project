from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'steam_id', 'skill_level', 'is_active')
    list_filter = ('skill_level', 'play_style', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'steam_id')
    
    fieldsets = UserAdmin.fieldsets + (
        ('게임 정보', {
            'fields': ('steam_id', 'discord_id', 'avatar', 'bio', 
                      'skill_level', 'play_style', 'preferred_time')
        }),
    )