from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Party, PartyMember, PartyComment
from games.serializers import GameListSerializer
from users.serializers import UserSerializer

User = get_user_model()


class PartyMemberSerializer(serializers.ModelSerializer):
    """파티 멤버 직렬화"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = PartyMember
        fields = ('user', 'joined_at', 'is_ready')


class PartyCommentSerializer(serializers.ModelSerializer):
    """파티 댓글 직렬화"""
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = PartyComment
        fields = ('id', 'author', 'content', 'parent', 'replies', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return PartyCommentSerializer(obj.replies.all(), many=True).data
        return []


class PartyListSerializer(serializers.ModelSerializer):
    """파티 목록 직렬화"""
    game = GameListSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    current_members_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Party
        fields = ('id', 'title', 'game', 'creator', 'max_members', 
                 'current_members_count', 'is_full', 'status', 
                 'play_time', 'required_skill', 'play_style', 
                 'voice_chat_required', 'created_at')


class PartyDetailSerializer(serializers.ModelSerializer):
    """파티 상세 직렬화"""
    game = GameListSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    members = PartyMemberSerializer(source='partymember_set', many=True, read_only=True)
    comments = PartyCommentSerializer(many=True, read_only=True)
    current_members_count = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    can_join = serializers.SerializerMethodField()
    
    class Meta:
        model = Party
        fields = '__all__'
        read_only_fields = ('creator', 'created_at', 'updated_at')
    
    def get_can_join(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.can_join(request.user)
        return False


class PartyCreateSerializer(serializers.ModelSerializer):
    """파티 생성 직렬화"""
    class Meta:
        model = Party
        fields = ('title', 'description', 'game', 'max_members', 
                 'play_time', 'duration_hours', 'required_skill', 
                 'play_style', 'voice_chat_required', 'discord_link')
    
    def create(self, validated_data):
        user = self.context['request'].user
        party = Party.objects.create(creator=user, **validated_data)
        # 생성자를 자동으로 파티 멤버로 추가
        PartyMember.objects.create(party=party, user=user)
        return party


class PartyUpdateSerializer(serializers.ModelSerializer):
    """파티 수정 직렬화"""
    class Meta:
        model = Party
        fields = ('title', 'description', 'max_members', 'status',
                 'play_time', 'duration_hours', 'required_skill',
                 'play_style', 'voice_chat_required', 'discord_link')