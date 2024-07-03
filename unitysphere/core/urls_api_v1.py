from django.urls import path, include

urlpatterns = [
    path('', include('clubs.api.urls')),
    path('', include('accounts.api.urls')),
]
