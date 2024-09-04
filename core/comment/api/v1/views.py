from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from blog.api.v1.permission import IsOwnerOrReadOnly
from comment.api.v1.serializers import CommentSerializers
from comment.models import Comment


class CommentViewSetsApiView(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user.profile
        queryset = Comment.objects.filter(author=user, approach=True)
        return queryset
