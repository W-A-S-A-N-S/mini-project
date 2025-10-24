from rest_framework import generics, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from .models import Game
from .serializers import GameSerializer, GameListSerializer
import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q


class GameListView(generics.ListAPIView):
    """게임 목록 조회"""
    serializer_class = GameListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'difficulty', 'is_popular']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'is_popular', 'open_party_count']
    ordering = ['-open_party_count']

    def get_queryset(self):
        return Game.objects.annotate(
            open_party_count=Count('parties', filter=Q(parties__status='open'))
        )


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


class GameSearchView(APIView):
    """
    Steam 게임 검색
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response([], status=status.HTTP_200_OK)

        steam_games = cache.get('steam_games')
        if not steam_games:
            try:
                response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
                response.raise_for_status()
                steam_games = response.json()['applist']['apps']
                cache.set('steam_games', steam_games, 60 * 60 * 24)  # Cache for 24 hours
            except requests.RequestException as e:
                return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        search_results = [
            game for game in steam_games
            if query.lower() in game['name'].lower()
        ][:20]  # Limit to 20 results

        return Response(search_results, status=status.HTTP_200_OK)