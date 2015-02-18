from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.api import project_router

urlpatterns = patterns('',
    # Examples:
    url(r'^api/v1/', include(project_router.urls)), 
    url(r'^admin/', include(admin.site.urls)),
)
