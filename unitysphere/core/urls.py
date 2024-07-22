from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django import views as django_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls_api_v1')),
    path('accounts/', include('accounts.urls')),
    path('', include('clubs.urls')),
    re_path(r'^jsi18n/$', django_views.i18n.JavaScriptCatalog.as_view(), name='jsi18n')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
