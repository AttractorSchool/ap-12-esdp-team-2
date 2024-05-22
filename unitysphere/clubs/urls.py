from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('clubs', views.ClubViewSet)
router.register('category', views.ClubCategoryViewSet)
router.register('cities', views.ClubCityViewSet)
router.register('services', views.ClubServiceViewSet)
router.register('events', views.ClubEventViewSet)
router.register('ads', views.ClubAdsViewSet)
urlpatterns = router.urls
