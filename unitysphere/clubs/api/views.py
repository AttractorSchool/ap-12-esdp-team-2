from rest_framework import generics, permissions, viewsets

from clubs.api.serializers import ClubSerializer, ClubCategorySerializer
from clubs.models import Club, ClubCategory


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.filter(is_active=True)
    serializer_class = ClubSerializer


class ClubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClubCategory.objects.all()
    serializer_class = ClubCategorySerializer
