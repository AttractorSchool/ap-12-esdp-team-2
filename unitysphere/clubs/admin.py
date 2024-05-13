from django.contrib import admin
from .models import *


@admin.register(Club)
class CutomClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'address')


@admin.register(ClubCategory)
class CutomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(ClubEvent)
class CustomClubEventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'location',
        'start_datetime',
        'end_datetime',
        'club',
    )


@admin.register(ClubAds)
class CustomClubAdsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'club',
        'type',
    )
