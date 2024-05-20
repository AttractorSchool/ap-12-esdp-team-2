from rest_framework import serializers
from clubs.models import Club, ClubCategory, City
from accounts.api.serializers import UserReadSerializer


class ClubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ClubCategory
        fields = ('id', 'name')


class ClubCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'name')


class ClubReadSerializer(serializers.ModelSerializer):
    category = ClubCategorySerializer()
    city = ClubCitySerializer()
    creater = UserReadSerializer()
    members = UserReadSerializer(many=True)
    likes = UserReadSerializer(many=True)
    partners = UserReadSerializer(many=True)
    managers = UserReadSerializer(many=True)

    class Meta:

        model = Club
        fields = '__all__'


class ClubCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Club
        fields = '__all__'
