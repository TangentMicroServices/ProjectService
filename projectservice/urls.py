from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.api import project_router
from health import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    
    url(r'^explorer/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^health/', api.health),
    url(r'^', include(project_router.urls)), 
    
)

if settings.DEBUG is True:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
