from django.urls import path
from . import views as api_views

urlpatterns = [
    path('register', api_views.UserCreateAPIView.as_view()),
    path('login', api_views.UserLoginAPIView.as_view()),
    path('account/verify', api_views.UserVerifyAPIView.as_view()),
]