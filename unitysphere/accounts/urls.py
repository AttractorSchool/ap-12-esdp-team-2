from django.contrib.auth.views import LogoutView
from django.urls import path
from .api.urls import urlpatterns as accounts_api_urls
from accounts import views
from api import views as api_views

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('<uuid:pk>/detail/', views.UserDetailView.as_view(), name='user_detail'),
    path('edit/', views.UserUpdateView.as_view(), name='user_update'),
]
