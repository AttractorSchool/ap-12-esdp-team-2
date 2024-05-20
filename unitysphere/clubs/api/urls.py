from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'club_objects', views.ClubViewSet)
router.register(r'category', views.ClubCategoryViewSet)
urlpatterns = router.urls
