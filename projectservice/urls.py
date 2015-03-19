from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.api import project_router
from health import api

urlpatterns = patterns('',
    url(r'^api/v1/', include(project_router.urls)), 
    url(r'^api-explorer/', include('rest_framework_swagger.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', api.health),
)
