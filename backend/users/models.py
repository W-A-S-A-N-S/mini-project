from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """커스텀 User 모델"""
    steam_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    discord_id = models.CharField(max_length=100, blank=True)
    
    # 게임 관련 필드
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', '초보'),
            ('intermediate', '중급'),
            ('advanced', '고급'),
            ('expert', '전문가'),
        ],
        default='beginner'
    )
    
    play_style = models.CharField(
        max_length=20,
        choices=[
            ('casual', '캐주얼'),
            ('serious', '진지함'),
            ('competitive', '경쟁적'),
            ('fun', '재미 위주'),
        ],
        default='casual'
    )
    
    preferred_time = models.JSONField(default=list, blank=True)  # 선호 시간대
    preferred_games = models.ManyToManyField('games.Game', blank=True, related_name='preferred_by')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자들'
    
    def __str__(self):
        return self.username