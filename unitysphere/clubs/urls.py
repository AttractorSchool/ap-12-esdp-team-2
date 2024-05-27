from django.urls import path

from . import views
from rest_framework import routers
from rest_framework.decorators import action

router = routers.DefaultRouter()
router.register('clubs', views.ClubViewSet)
router.register('category', views.ClubCategoryViewSet)
router.register('cities', views.ClubCityViewSet)
router.register('services', views.ClubServiceViewSet)
router.register('events', views.ClubEventViewSet)
router.register('ads', views.ClubAdsViewSet)
router.register('gallery/photos', views.ClubGalleryPhotoViewSet)
router.register('festivals', views.FestivalViewSet)
router.register('festival/requests', views.FestivalParticipationRequestViewSet)

urlpatterns = router.urls
