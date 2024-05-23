from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from clubs import models
from .permissions import ClubPermission, ClubObjectsPermission
from . import exeptions as club_exceptions
from . import mixins


class ClubViewSet(mixins.ClubActionSerializerMixin, viewsets.ModelViewSet):
    queryset = models.Club.objects.filter(is_active=True)
    permission_classes = (ClubPermission,)
    ACTION_SERIALIZERS = {
        'club_action': serializers.ClubActionSerializer,
        'create': serializers.ClubCreateSerializer,
        'update': serializers.ClubUpdateSerializer,
    }
    serializer_class = serializers.ClubReadSerializer

    @action(detail=True, methods=['post'])
    def club_action(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        club = self.get_object()
        action_name = serializer.validated_data['action']
        getattr(club, action_name)(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClubServiceViewSet(viewsets.ModelViewSet):
    queryset = models.ClubService.objects.all()
    permission_classes = (ClubObjectsPermission,)
    serializer_class = serializers.ClubServiceSerializer


class ClubEventViewSet(viewsets.ModelViewSet):
    queryset = models.ClubEvent.objects.filter(start_datetime__gte=datetime.now())
    permission_classes = (ClubObjectsPermission, )
    serializer_class = serializers.ClubEventSerializer


class ClubAdsViewSet(viewsets.ModelViewSet):
    queryset = models.ClubAds.objects.all()
    permission_classes = (ClubObjectsPermission, )
    serializer_class = serializers.ClubAdsSerializer


class ClubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ClubCategory.objects.filter(is_active=True)
    serializer_class = serializers.ClubCategorySerializer


class ClubCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.ClubCitySerializer


class ClubGalleryPhotoViewSet(viewsets.ModelViewSet):
    queryset = models.ClubGalleryPhoto.objects.all()
    permission_classes = (ClubObjectsPermission,)
    serializer_class = serializers.ClubGalleryPhotoSerializer
