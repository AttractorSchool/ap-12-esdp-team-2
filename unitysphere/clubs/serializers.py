from enum import StrEnum

from rest_framework import serializers
from clubs import models
from accounts.api.serializers import UserReadSerializer


class ClubActionEnum(StrEnum):
    UNLIKE = 'unlike'
    LIKE = 'like'
    JOIN = 'join'
    LEAVE = 'leave'


class FestivalActionEnum(StrEnum):
    JOIN = 'join'
    LEAVE = 'leave'


class RequestActionEnum(StrEnum):
    APPROVE = 'approve'
    REJECT = 'reject'


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
        fields = ('name', 'category', 'logo', 'creater', 'email', 'phone', 'description', 'is_private')

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


class ClubListSerializer(serializers.ModelSerializer):
    category = ClubCategorySerializer()

    class Meta:
        model = models.Club
        fields = (
            'id',
            'name',
            'category',
            'logo',
            'description',
            'members_count',
            'likes_count',
            'is_private',
            'created_at',
        )


class ClubDetailSerializer(serializers.ModelSerializer):
    category = ClubCategorySerializer()
    city = ClubCitySerializer()
    members = UserReadSerializer(many=True)
    likes = UserReadSerializer(many=True)
    partners = ClubListSerializer(many=True)
    creater = UserReadSerializer()
    managers = UserReadSerializer(many=True)

    class Meta:
        model = models.Club
        fields = '__all__'


class ClubSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Club
        fields = ('id', 'name')


class ClubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClubService
        fields = '__all__'


class ClubServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClubServiceImage
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


class FestivalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Festival
        fields = ('id', 'name', 'description', 'image')


class FestivalRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Festival
        fields = '__all__'


class FestivalCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Festival
        fields = ('name', 'description', 'image', 'location', 'start_datetime')


class FestivalActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=FestivalActionEnum)
    club = serializers.PrimaryKeyRelatedField(queryset=models.Club.objects.filter(is_active=True))


class FestivalSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Festival
        fields = ('id', 'name')


class FestivalRequestSerializer(serializers.ModelSerializer):
    club = ClubSimpleSerializer()
    festival = FestivalSimpleSerializer()

    class Meta:
        model = models.FestivalParticipationRequest
        fields = ('id', 'club', 'festival')


class FestivalRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=RequestActionEnum)


class ClubJoinRequestSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    club = ClubSimpleSerializer()

    class Meta:
        model = models.ClubJoinRequest
        fields = ('id', 'user', 'club')


class ClubJoinRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=RequestActionEnum)
