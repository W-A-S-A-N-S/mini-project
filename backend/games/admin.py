from django.contrib import admin
from .models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'max_players', 'difficulty', 'is_popular', 'created_at')
    list_filter = ('genre', 'difficulty', 'is_popular')
    search_fields = ('name', 'description', 'steam_app_id')
    list_editable = ('is_popular',)
    ordering = ('-is_popular', 'name')
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'steam_app_id', 'description', 'image_url')
        }),
        ('게임 특성', {
            'fields': ('genre', 'max_players', 'min_players', 'difficulty', 'is_popular')
        }),
        ('기타', {
            'fields': ('release_date',)
        }),
    )