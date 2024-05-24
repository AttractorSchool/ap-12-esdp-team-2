from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from clubs import models
from .permissions import ClubPermission, ClubObjectsPermission
from . import services
from . import mixins


class ClubViewSet(mixins.ClubActionSerializerMixin, viewsets.ModelViewSet):
    queryset = models.Club.objects.filter(is_active=True)
    permission_classes = (ClubPermission,)
    ACTION_SERIALIZERS = {
        'club_action': serializers.ClubActionSerializer,
        'create': serializers.ClubCreateSerializer,
        'update': serializers.ClubUpdateSerializer,
        'retrieve': serializers.ClubDetailSerializer,
    }
    serializer_class = serializers.ClubListSerializer

    @action(detail=True, methods=['post'])
    def club_action(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        club = self.get_object()
        club_services = services.ClubServices(club)
        action_name = serializer.validated_data['action']
        getattr(club_services, action_name)(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == 'retrieve':
            return (
                queryset.
                select_related('category', 'city', 'creater').
                prefetch_related('members', 'partners', 'likes', 'managers'))
        return queryset


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
