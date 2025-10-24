from django.urls import path
from .views import ProfileView, UserDetailView

app_name = 'users_profile'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]