from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


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
    def get_object(self, pk):
        try:
            profile = profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404
