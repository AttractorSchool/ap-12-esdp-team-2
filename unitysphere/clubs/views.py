from django.views import generic

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from . import serializers, models


class IndexView(generic.TemplateView):
    template_name = 'clubs/index.html'


class ClubViewSet(viewsets.ModelViewSet):

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return (IsAuthenticated(),)

        return (AllowAny(),)

    def get_queryset(self):
        return models.Club.objects.filter(creator=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateClubSerializer

        return serializers.ListClubSerializer
