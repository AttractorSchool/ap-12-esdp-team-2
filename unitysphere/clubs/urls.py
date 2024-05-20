from django.urls import path
from . import views as clubs_views

urlpatterns = [
    path('', clubs_views.IndexView.as_view(), name='index'),
]
