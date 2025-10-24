from django.urls import path
from .views import GameListView, GameDetailView, PopularGameListView, GameSearchView

app_name = 'games'

urlpatterns = [
    path('', GameListView.as_view(), name='game_list'),
    path('popular/', PopularGameListView.as_view(), name='popular_games'),
    path('search/', GameSearchView.as_view(), name='game_search'),
    path('<int:pk>/', GameDetailView.as_view(), name='game_detail'),
]