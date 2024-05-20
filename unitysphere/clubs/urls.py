from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('clubs', views.ClubViewSet, basename='clubs')


urlpatterns = router.urls
