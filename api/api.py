from django.conf.urls import url, include
from models import Project
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project        

# ViewSets define the view behavior.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# Routers provide an easy way of automatically determining the URL conf.
project_router = routers.DefaultRouter()
project_router.register('projects', ProjectViewSet)