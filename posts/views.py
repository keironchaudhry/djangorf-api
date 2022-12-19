from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):
    def get(self, request):
        # Like in profile app, retrieve all post objects,
        posts = Post.objects.all()
        # Serialize them,
        serializer = PostSerializer(
            post,
            many=True,
            context={'request': request}
        )
        # And return serialized data using Response
        return Response(
            serializer.data
        )
