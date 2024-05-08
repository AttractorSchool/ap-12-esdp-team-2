from django.contrib import admin
from .models import Club, ClubCategory, City 


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'logo',
        'managers', 'description', 
        'email', 'phone', 'city', 
        'address', 'is_active',
    )


@admin.register(ClubCategory)
class ClubCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'is_active',
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'iata_code',
    )
