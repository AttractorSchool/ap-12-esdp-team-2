from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from clubs import models
from .permissions import ClubPermission, ClubObjectsPermission
from . import exeptions as club_exceptions


class ClubViewSet(viewsets.ModelViewSet):
    queryset = models.Club.objects.filter(is_active=True)
    permission_classes = [ClubPermission,]

    @action(detail=True, methods=['post'])
    def club_action(self, request, **kwargs):
        club = self.get_object()
        user = request.user
        action_name = request.query_params.get('action')
        if action_name == 'join':
            club.join(user)
        elif action_name == 'leave':
            club.leave(user)
        elif action_name == 'like':
            club.like(user)
        elif action_name == 'unlike':
            club.unlike(user)
        else:
            raise club_exceptions.InvalidClubActionExeption
        return Response({'detail': 'Success'}, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.ClubCreateSerializer
        return serializers.ClubReadSerializer


class ClubServiceViewSet(viewsets.ModelViewSet):
    queryset = models.ClubService.objects.all()
    permission_classes = [ClubObjectsPermission, ]
    serializer_class = serializers.ClubServiceSerializer


class ClubEventViewSet(viewsets.ModelViewSet):
    queryset = models.ClubEvent.objects.filter(start_datetime__gte=datetime.now())
    permission_classes = [ClubObjectsPermission, ]
    serializer_class = serializers.ClubEventSerializer


class ClubAdsViewSet(viewsets.ModelViewSet):
    queryset = models.ClubAds.objects.all()
    permission_classes = [ClubObjectsPermission, ]
    serializer_class = serializers.ClubAdsSerializer


class ClubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ClubCategory.objects.filter(is_active=True)
    serializer_class = serializers.ClubCategorySerializer


class ClubCityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.ClubCitySerializer


class ClubGalleryPhotoViewSet(viewsets.ModelViewSet):
    queryset = models.ClubGalleryPhoto.objects.all()
    permission_classes = [ClubObjectsPermission, ]
    serializer_class = serializers.ClubGalleryPhotoSerializer
