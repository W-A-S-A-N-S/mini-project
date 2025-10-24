from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    """게임 직렬화"""
    active_parties_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class GameListSerializer(serializers.ModelSerializer):
    """게임 목록 직렬화 (간단한 정보만)"""
    active_parties_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Game
        fields = ('id', 'name', 'image_url', 'genre', 'max_players', 
                 'min_players', 'difficulty', 'is_popular', 'active_parties_count')