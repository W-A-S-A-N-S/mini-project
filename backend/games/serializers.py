from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    """게임 직렬화"""
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class GameListSerializer(serializers.ModelSerializer):
    """게임 목록 직렬화 (간단한 정보만)"""
    open_party_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Game
        fields = ('id', 'name', 'image_url', 'genre', 'max_players', 
                 'min_players', 'difficulty', 'is_popular', 'open_party_count')