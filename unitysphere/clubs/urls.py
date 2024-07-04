from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('clubs/', views.ClubListView.as_view(), name='clubs'),
    path('clubs/create/', views.ClubCreateView.as_view(), name='club_create'),
    path('clubs/<uuid:pk>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('clubs/<uuid:pk>/photogallery/', views.ClubPhotoGalleryView.as_view(), name='club_photogallery'),
    path('clubs/<uuid:pk>/update', views.ClubEditView.as_view(), name='club_edit'),
    path('clubs/<uuid:pk>/managers/edit/', views.ChooseClubManagersView.as_view(), name='club_managers_choose'),
    path('category/<uuid:pk>/', views.CategoryClubsView.as_view(), name='category_detail'),
    path('club/events/', views.ClubEventListView.as_view(), name='club_events'),
    path('club/<uuid:pk>/events/create/', views.CreateClubEventView.as_view(), name='event_create'),
    path('club/events/<uuid:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event-calendar/', views.EventCalendarView.as_view(), name='event_calendar'),
    path('about/', views.AboutView.as_view(), name='about')
]
