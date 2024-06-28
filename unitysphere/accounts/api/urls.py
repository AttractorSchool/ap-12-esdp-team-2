from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views as api_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', api_views.UserCreateAPIView.as_view()),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('profile/<uuid:pk>/update/', api_views.ProfileUpdateAPIView.as_view(), name='update_profile'),
]
