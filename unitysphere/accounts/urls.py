from django.urls import path
from .api.urls import urlpatterns as accounts_api_urls
from accounts import views


urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
] + accounts_api_urls
