from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# In this walkthrough, rather than repeating
# the creation of a GET, PUT, POST, DELETE etc.,
# we have imported 'generics' and using built in features
# that enable the creation of these methods.


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )
