from django.conf.urls import url, include
from models import Project, Resource, Task
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import detail_route, list_route
import os

# Serializers define the API representation.
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project        

# ViewSets define the view behavior.
class ProjectViewSet(viewsets.ModelViewSet):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @detail_route(methods=['post'])
    def setup(self, request, pk=None):
        '''
        TBD:
        * Create Pivotal, Github, Hipchat
        * Create webhook in github to pivotal, hipchat 
        * Create webhook in pivotal to github
        '''

        print os.environ['PIVOTAL_TOKEN']
        print os.environ['HIPCHAT_TOKEN']
        print os.environ['GITHUB_TOKEN']


# Serializers define the API representation.
class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource        

# ViewSets define the view behavior.
class ResourceViewSet(viewsets.ModelViewSet):
    
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task        

# ViewSets define the view behavior.
class TaskViewSet(viewsets.ModelViewSet):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
        

# Routers provide an easy way of automatically determining the URL conf.
project_router = routers.DefaultRouter()
project_router.register('projects', ProjectViewSet)
project_router.register('resources', ResourceViewSet)
project_router.register('tasks', TaskViewSet)