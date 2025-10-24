from django.db import models


class Game(models.Model):
    """게임 모델"""
    name = models.CharField(max_length=200, unique=True)
    steam_app_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    
    genre = models.CharField(
        max_length=50,
        choices=[
            ('fps', 'FPS'),
            ('rpg', 'RPG'),
            ('moba', 'MOBA'),
            ('survival', 'Survival'),
            ('strategy', 'Strategy'),
            ('puzzle', 'Puzzle'),
            ('adventure', 'Adventure'),
            ('simulation', 'Simulation'),
            ('other', 'Other'),
        ],
        default='other'
    )
    
    max_players = models.IntegerField(default=4)
    min_players = models.IntegerField(default=2)
    
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', '쉬움'),
            ('normal', '보통'),
            ('hard', '어려움'),
            ('extreme', '매우 어려움'),
        ],
        default='normal'
    )
    
    is_popular = models.BooleanField(default=False)
    release_date = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'games'
        verbose_name = '게임'
        verbose_name_plural = '게임들'
        ordering = ['-is_popular', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def active_parties_count(self):
        """활성 파티 수"""
        return self.parties.filter(status='open').count()