from rest_framework import permissions


class IsPartyCreatorOrReadOnly(permissions.BasePermission):
    """파티 생성자만 수정/삭제 가능"""
    
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 쓰기 권한은 파티 생성자에게만 허용
        return obj.creator == request.user


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """댓글 작성자만 수정/삭제 가능"""
    
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모두에게 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 쓰기 권한은 댓글 작성자에게만 허용
        return obj.author == request.user