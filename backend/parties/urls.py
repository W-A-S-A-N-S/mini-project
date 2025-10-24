from django.urls import path
from .views import (
    PartyListView, PartyDetailView, 
    PartyJoinView, PartyLeaveView, MyPartiesView,
    PartyCommentListCreateView, PartyCommentDetailView
)

app_name = 'parties'

urlpatterns = [
    path('', PartyListView.as_view(), name='party_list'),
    path('my/', MyPartiesView.as_view(), name='my_parties'),
    path('<int:pk>/', PartyDetailView.as_view(), name='party_detail'),
    path('<int:pk>/join/', PartyJoinView.as_view(), name='party_join'),
    path('<int:pk>/leave/', PartyLeaveView.as_view(), name='party_leave'),
    path('<int:party_id>/comments/', PartyCommentListCreateView.as_view(), name='party_comments'),
    path('comments/<int:pk>/', PartyCommentDetailView.as_view(), name='comment_detail'),
]