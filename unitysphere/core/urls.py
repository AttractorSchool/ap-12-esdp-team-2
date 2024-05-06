from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('accounts.urls')),

    path('api/v1/', include('api.urls')),

    path('', include('clubs.urls')),
]
