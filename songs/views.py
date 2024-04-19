from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework.generics import ListCreateAPIView

from ipdb import set_trace

class SongView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return self.queryset.filter(album__id=pk)
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        album = get_object_or_404(Album, pk=pk)
        serializer.save(album=album)

