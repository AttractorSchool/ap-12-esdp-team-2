from rest_framework import serializers
from clubs.models import Club, ClubCategory


class ClubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ClubCategory
        fields = ('id', 'name')


class ClubSerializer(serializers.ModelSerializer):
    category = ClubCategorySerializer()

    class Meta:

        model = Club
        fields = '__all__'


