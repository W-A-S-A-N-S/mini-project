from django.contrib import admin
from .models import Party, PartyMember, PartyComment


class PartyMemberInline(admin.TabularInline):
    model = PartyMember
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'creator', 'status', 'max_members', 
                   'current_members_count', 'play_time', 'created_at')
    list_filter = ('status', 'game', 'required_skill', 'play_style', 'voice_chat_required')
    search_fields = ('title', 'description', 'game__name', 'creator__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PartyMemberInline]
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'description', 'game', 'creator')
        }),
        ('파티 설정', {
            'fields': ('max_members', 'status', 'play_time', 'duration_hours')
        }),
        ('매칭 조건', {
            'fields': ('required_skill', 'play_style', 'voice_chat_required', 'discord_link')
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PartyMember)
class PartyMemberAdmin(admin.ModelAdmin):
    list_display = ('party', 'user', 'joined_at', 'is_ready')
    list_filter = ('is_ready', 'joined_at')
    search_fields = ('party__title', 'user__username')


@admin.register(PartyComment)
class PartyCommentAdmin(admin.ModelAdmin):
    list_display = ('party', 'author', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('party__title', 'author__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '내용 미리보기'