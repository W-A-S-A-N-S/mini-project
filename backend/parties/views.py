from rest_framework import generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Party, PartyMember, PartyComment
from .serializers import (
    PartyListSerializer, PartyDetailSerializer,
    PartyCreateSerializer, PartyUpdateSerializer,
    PartyCommentSerializer
)
from .permissions import IsPartyCreatorOrReadOnly, IsCommentAuthorOrReadOnly


class PartyListView(generics.ListCreateAPIView):
    """파티 목록 조회 및 생성"""
    queryset = Party.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['game', 'status', 'required_skill', 'play_style', 'voice_chat_required']
    search_fields = ['title', 'description', 'game__name']
    ordering_fields = ['created_at', 'play_time']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PartyCreateSerializer
        return PartyListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]


class PartyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """파티 상세 조회, 수정, 삭제"""
    queryset = Party.objects.all()
    permission_classes = [IsPartyCreatorOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PartyUpdateSerializer
        return PartyDetailSerializer


class PartyJoinView(APIView):
    """파티 참가"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        party = get_object_or_404(Party, pk=pk)
        user = request.user
        
        if not party.can_join(user):
            return Response(
                {'error': '파티에 참가할 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        PartyMember.objects.create(party=party, user=user)
        
        # 파티가 가득 차면 자동으로 모집 마감
        if party.is_full:
            party.status = 'closed'
            party.save()
        
        return Response(
            {'message': '파티에 참가했습니다.'},
            status=status.HTTP_201_CREATED
        )


class PartyLeaveView(APIView):
    """파티 나가기"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        party = get_object_or_404(Party, pk=pk)
        user = request.user
        
        # 파티 생성자는 나갈 수 없음
        if party.creator == user:
            return Response(
                {'error': '파티 생성자는 파티를 나갈 수 없습니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        member = PartyMember.objects.filter(party=party, user=user).first()
        if not member:
            return Response(
                {'error': '파티 멤버가 아닙니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        member.delete()
        
        # 파티에 자리가 생기면 다시 모집 중으로 변경
        if party.status == 'closed' and not party.is_full:
            party.status = 'open'
            party.save()
        
        return Response(
            {'message': '파티에서 나갔습니다.'},
            status=status.HTTP_200_OK
        )


class MyPartiesView(generics.ListAPIView):
    """내가 참가 중인 파티 목록"""
    serializer_class = PartyListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Party.objects.filter(members=self.request.user)


class PartyCommentListCreateView(generics.ListCreateAPIView):
    """파티 댓글 목록 조회 및 생성"""
    serializer_class = PartyCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        party_id = self.kwargs.get('party_id')
        return PartyComment.objects.filter(party_id=party_id, parent=None)
    
    def perform_create(self, serializer):
        party = get_object_or_404(Party, pk=self.kwargs.get('party_id'))
        serializer.save(author=self.request.user, party=party)


class PartyCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """파티 댓글 상세, 수정, 삭제"""
    queryset = PartyComment.objects.all()
    serializer_class = PartyCommentSerializer
    permission_classes = [IsCommentAuthorOrReadOnly]