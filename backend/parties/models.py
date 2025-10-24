from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Party(models.Model):
    """파티 모델"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='parties')
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_parties')
    members = models.ManyToManyField(User, through='PartyMember', related_name='joined_parties')
    
    max_members = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(10)],
        default=4
    )
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', '모집 중'),
            ('closed', '모집 마감'),
            ('in_progress', '진행 중'),
            ('completed', '완료'),
        ],
        default='open'
    )
    
    play_time = models.DateTimeField()  # 플레이 예정 시간
    duration_hours = models.IntegerField(default=2)  # 예상 플레이 시간
    
    required_skill = models.CharField(
        max_length=20,
        choices=[
            ('any', '무관'),
            ('beginner', '초보'),
            ('intermediate', '중급'),
            ('advanced', '고급'),
            ('expert', '전문가'),
        ],
        default='any'
    )
    
    play_style = models.CharField(
        max_length=20,
        choices=[
            ('any', '무관'),
            ('casual', '캐주얼'),
            ('serious', '진지함'),
            ('competitive', '경쟁적'),
            ('fun', '재미 위주'),
        ],
        default='any'
    )
    
    voice_chat_required = models.BooleanField(default=False)
    discord_link = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'parties'
        verbose_name = '파티'
        verbose_name_plural = '파티들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.game.name} - {self.title}"
    
    @property
    def current_members_count(self):
        return self.members.count()
    
    @property
    def is_full(self):
        return self.current_members_count >= self.max_members
    
    def can_join(self, user):
        """사용자가 파티에 참가 가능한지 확인"""
        if self.is_full:
            return False
        if self.status != 'open':
            return False
        if user in self.members.all():
            return False
        return True


class PartyMember(models.Model):
    """파티 멤버 중간 테이블"""
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_ready = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'party_members'
        unique_together = ('party', 'user')
        verbose_name = '파티 멤버'
        verbose_name_plural = '파티 멤버들'
    
    def __str__(self):
        return f"{self.party.title} - {self.user.username}"


class PartyComment(models.Model):
    """파티 댓글"""
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'party_comments'
        verbose_name = '파티 댓글'
        verbose_name_plural = '파티 댓글들'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.party.title} - {self.author.username}: {self.content[:30]}"