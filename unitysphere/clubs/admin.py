from django.contrib import admin
from .models import *


class CutomClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'address')


admin.site.register(Club, CutomClubAdmin)


class CutomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


admin.site.register(ClubCategory, CutomCategoryAdmin)
