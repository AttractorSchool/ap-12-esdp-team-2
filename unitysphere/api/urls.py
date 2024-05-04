from django.urls import path
from . import views as api_views

urlpatterns = [
    path('register', api_views.UserCreateAPIView.as_view()),
    path('register/verify', api_views.UserVerifyAPIView.as_view()),
]