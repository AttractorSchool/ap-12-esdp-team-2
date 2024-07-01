from django.urls import path, include

urlpatterns = [
    path('', include('clubs.urls')),
    path('', include('accounts.api.urls')),
]
