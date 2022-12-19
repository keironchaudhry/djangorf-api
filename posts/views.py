from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostList(APIView):

    # Creates a post form to be rendered on page
    serializer_class = PostSerializer
    # Permissions and authentication for user
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        # Like in profile app, retrieve all post objects,
        posts = Post.objects.all()
        # Serialize them,
        serializer = PostSerializer(
            posts,
            many=True,
            context={'request': request}
        )
        # And return serialized data using Response
        return Response(
            serializer.data
        )

    def post(self, request):
        # Deserialize the user data
        serializer = PostSerializer(
            data=request.data,
            context={'request': request}
        )
        # Passes in save method on serializer
        # and identifies the user making the request
        if serializer.is_valid():
            serializer.save(owner=request.user)
            # Returns the serialized data with
            # 201 status is serializer is valid
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        # Else returns 400 bad request if invalid
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
