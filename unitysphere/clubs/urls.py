from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('clubs/', views.ClubListView.as_view(), name='clubs'),
    path('clubs/<uuid:pk>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('category/<uuid:pk>/', views.CategoryClubsView.as_view(), name='category_detail'),
    path('club/events/', views.ClubEventListView.as_view(), name='club_events'),
    path('club/events/<uuid:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event-calendar/', views.EventCalendarView.as_view(), name='event_calendar'),
    path('about/', views.AboutView.as_view(), name='about'),
]
