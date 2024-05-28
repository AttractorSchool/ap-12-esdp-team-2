from django_filters import rest_framework as filters

from clubs import models


class ClubFilter(filters.FilterSet):

    class Meta:
        model = models.Club
        fields = ('is_private', 'members', 'managers')
