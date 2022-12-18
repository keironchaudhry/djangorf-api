from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    """
    List all profiles
    No Create view (post method), as profile creation handled by django signals
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles,
            many=True
        )
        return Response(
            serializer.data
        )


class ProfileDetail(APIView):
    # Allows serialized code to be modified with a form
    serializer_class = ProfileSerializer
    # Inherits the permission class created and imported in this file
    permission_classes = [IsOwnerOrReadOnly]

    # Simple get object method to obtain actual
    # profile object or return an error page
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(
                pk=pk
            )
            # Accesses the permissions class created to validate user permissions
            self.check_object_permissions(
                self.request,
                profile
            )
            return profile
        except Profile.DoesNotExist:
            raise Http404

    # Simple get method to obtain data and
    # serialize said data into readable JSON code
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(
            serializer.data
        )

    # Put method to obtain profile object via pk
    # that allows us to modify data and save it
    # or in the case of error, throws a 400 error
    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
