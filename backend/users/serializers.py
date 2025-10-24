from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'steam_id')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """일반 User 직렬화"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'steam_id', 'avatar', 'bio', 
                 'discord_id', 'skill_level', 'play_style', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserProfileSerializer(serializers.ModelSerializer):
    """User 프로필 직렬화"""
    preferred_games = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    parties_created = serializers.SerializerMethodField()
    parties_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'steam_id', 'avatar', 'bio',
                 'discord_id', 'skill_level', 'play_style', 'preferred_time',
                 'preferred_games', 'parties_created', 'parties_joined', 
                 'created_at', 'updated_at')
        read_only_fields = ('id', 'username', 'created_at', 'updated_at')
    
    def get_parties_created(self, obj):
        return obj.created_parties.count()
    
    def get_parties_joined(self, obj):
        return obj.joined_parties.count()


class UserUpdateSerializer(serializers.ModelSerializer):
    """User 정보 업데이트 직렬화"""
    class Meta:
        model = User
        fields = ('bio', 'discord_id', 'skill_level', 'play_style', 
                 'preferred_time', 'avatar')