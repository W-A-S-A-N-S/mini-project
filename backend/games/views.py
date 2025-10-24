from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .models import Game
from .serializers import GameSerializer, GameListSerializer


class GameListView(generics.ListAPIView):
    """게임 목록 조회"""
    queryset = Game.objects.all()
    serializer_class = GameListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'difficulty', 'is_popular']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'is_popular']
    ordering = ['-is_popular', 'name']


class GameDetailView(generics.RetrieveAPIView):
    """게임 상세 조회"""
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [AllowAny]


class PopularGameListView(generics.ListAPIView):
    """인기 게임 목록"""
    queryset = Game.objects.filter(is_popular=True)
    serializer_class = GameListSerializer
    permission_classes = [AllowAny]
    pagination_class = None