from enum import StrEnum

from rest_framework import serializers

from clubs import models
from clubs.serializers.club import ClubSimpleSerializer
from clubs.serializers.festival import FestivalSimpleSerializer


class RequestActionEnum(StrEnum):
    APPROVE = 'approve'
    REJECT = 'reject'


class FestivalRequestSerializer(serializers.ModelSerializer):
    club = ClubSimpleSerializer()
    festival = FestivalSimpleSerializer()

    class Meta:
        model = models.FestivalParticipationRequest
        fields = ('id', 'club', 'festival')


class FestivalRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=RequestActionEnum)
