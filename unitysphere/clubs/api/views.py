from rest_framework import generics, permissions, viewsets

from clubs.api import serializers
from clubs.models import Club, ClubCategory


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.filter(is_active=True)
    serializer_class = serializers.ClubReadSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return serializers.ClubReadSerializer
        elif self.action in ['create']:
            return serializers.ClubCreateSerializer
        else:
            return self.serializer_class


class ClubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClubCategory.objects.all()
    serializer_class = serializers.ClubCategorySerializer
