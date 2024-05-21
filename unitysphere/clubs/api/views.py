from datetime import datetime

from rest_framework import viewsets

from clubs.api import serializers
from clubs.models import Club, ClubCategory, City, ClubService, ClubEvent, ClubAds
from .permissions import ClubPermission, ClubObjectsPermission
from .serializers import ClubServiceSerializer, ClubEventSerializer, ClubAdsSerializer


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.filter(is_active=True)
    permission_classes = [ClubPermission,]

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ClubCreateSerializer
        return serializers.ClubReadSerializer


class ClubServiceViewSet(viewsets.ModelViewSet):
    queryset = ClubService.objects.all()
    permission_classes = [ClubObjectsPermission, ]
    serializer_class = ClubServiceSerializer


class ClubEventViewSet(viewsets.ModelViewSet):
    queryset = ClubEvent.objects.filter(start_datetime__gte=datetime.now())
    permission_classes = [ClubObjectsPermission, ]
    serializer_class = ClubEventSerializer


class ClubAdsViewSet(viewsets.ModelViewSet):
    queryset = ClubAds.objects.all()
    permission_classes = [ClubObjectsPermission, ]
    serializer_class = ClubAdsSerializer


class ClubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClubCategory.objects.filter(is_active=True)
    serializer_class = serializers.ClubCategorySerializer


class ClubCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = serializers.ClubCitySerializer
