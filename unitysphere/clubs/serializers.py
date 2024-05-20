from rest_framework import serializers

from . import models


class CreateClubSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault)

    class Meta:
        model = models.Club
        fields = ('id', 'name', 'description')


class ListClubSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Club
        fields = '__all__'
