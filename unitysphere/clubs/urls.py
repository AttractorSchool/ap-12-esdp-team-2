from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('clubs/<uuid:pk>', views.ClubDetailView.as_view(), name='club_detail'),
]
