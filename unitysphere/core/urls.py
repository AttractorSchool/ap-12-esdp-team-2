from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.api.urls')),
    path('api/v1/clubs/', include('clubs.api.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('clubs.urls')),
]
