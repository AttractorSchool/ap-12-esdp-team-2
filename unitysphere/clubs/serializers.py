from enum import StrEnum

from rest_framework import serializers
from clubs import models
from accounts.api.serializers import UserReadSerializer


class ClubActionEnum(StrEnum):
    UNLIKE = 'unlike'
    LIKE = 'like'
    JOIN = 'join'
    LEAVE = 'leave'


class ClubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClubCategory
        fields = ('id', 'name')


class ClubCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = ('id', 'name')


class ClubCreateSerializer(serializers.ModelSerializer):
    creater = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Club
        fields = ('name', 'category', 'logo', 'creater', 'email', 'phone', 'description')

    def create(self, validated_data):
        club = models.Club(**validated_data)
        club.save()
        club.managers.add(validated_data['creater'])
        return club


class ClubUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Club
        fields = '__all__'


class ClubActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=ClubActionEnum)


class ClubReadSerializer(serializers.ModelSerializer):
    creater = UserReadSerializer()
    managers = UserReadSerializer(many=True)
    likes = UserReadSerializer(many=True)
    members = UserReadSerializer(many=True)

    class Meta:
        model = models.Club
        fields = '__all__'


class ClubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClubService
        fields = '__all__'


class ClubEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClubEvent
        exclude = ('old_datetime', )


class ClubAdsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClubAds
        fields = '__all__'


class ClubGalleryPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ClubGalleryPhoto
        fields = '__all__'
