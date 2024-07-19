from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('clubs/', views.ClubListView.as_view(), name='clubs'),
    path('clubs/create/', views.ClubCreateView.as_view(), name='club_create'),
    path('clubs/<uuid:pk>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('clubs/<uuid:pk>/create_service', views.CreateServiceView.as_view(), name='create_service'),
    path('clubs/<uuid:pk>/photogallery/', views.ClubPhotoGalleryView.as_view(), name='club_photogallery'),
    path('clubs/<uuid:pk>/photogallery/add/', views.ClubAddPhotoView.as_view(), name='club_photogallery_add'),
    path('clubs/<uuid:pk>/update', views.ClubEditView.as_view(), name='club_edit'),
    path('clubs/<uuid:pk>/managers/edit/', views.ChooseClubManagersView.as_view(), name='club_managers_choose'),
    path('category/<uuid:pk>/', views.CategoryClubsView.as_view(), name='category_detail'),
    path('club/events/', views.ClubEventListView.as_view(), name='club_events'),
    path('club/<uuid:pk>/events/create/', views.CreateClubEventView.as_view(), name='event_create'),
    path('club/events/<uuid:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event-calendar/', views.EventCalendarView.as_view(), name='event_calendar'),
    path('about/', views.AboutView.as_view(), name='about'),

    path('festivals/', views.FestivalListView.as_view(), name='festivals'),
    path('festivals/<uuid:pk>/', views.FestivalDetailView.as_view(), name='festival_detail'),
    path('festivals/create/', views.FestivalCreateView.as_view(), name='festival_create'),
    path('festivals/<uuid:pk>/update/', views.FestivalUpdateView.as_view(), name='festival_update'),
    path('festivals/<uuid:pk>/delete/', views.FestivalDeleteView.as_view(), name='festival_delete'),
    path('festivals/<uuid:pk>/requests/', views.FestivalRequests.as_view(), name='festival_requests'),
    path('festivals/<uuid:pk>/approved/', views.FestivalDeleteView.as_view(), name='festival_delete'),

    path('service/<uuid:pk>/', views.ClubServiceDetailView.as_view(), name='service_detail'),
    path('services/<uuid:pk>/edit/', views.UpdateServiceView.as_view(), name='edit_service'),
]
