from django.conf.urls import url, include
from models import Project, Resource, Task
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import detail_route, list_route
import os
import django_filters

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task   
        

class TaskFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name="project__resource__user")

    due_before = django_filters.DateFilter(name="due_date", lookup_type='lte')
    due_after = django_filters.DateFilter(name="due_date", lookup_type='gte')

    min_hours = django_filters.NumberFilter(name="estimated_hours", lookup_type='gte')
    max_hours = django_filters.NumberFilter(name="estimated_hours", lookup_type='lte')

    class Meta:
        model = Task
        fields = ['user', 'due_before', 'due_after', 'min_hours', 'max_hours']


# ViewSets define the view behavior.
class TaskViewSet(viewsets.ModelViewSet):
    
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    search_fields = ('title')
    ordering_fields = ('estimated_hours', 'due_date', 'updated', 'created')

    # this is overwritten purely for the purpose of documentation for swagger
    def list(self, request, *args, **kwargs):
        """
        List/filter/search tasks.
        ---
          parameters_strategy: merge
          parameters:
            - name: user
              description: filter tasks by user_id
              required: false
              type: string
              paramType: query
            - name: due_before
              description: Find tasks due before the given date. Date format is YYYY-mm-dd
              required: false
              type: date
              paramType: query
            - name: due_after
              description: Find tasks due before the given date. Date format is YYYY-mm-dd
              required: false
              type: date
              paramType: query
            - name: min_hours
              description: Find tasks above the minimum estimated hours
              required: false
              type: integer
              paramType: query
            - name: max_hours
              description: Find tasks below the minimum estimated hours
              required: false
              type: integer
              paramType: query
            
            - name: ordering
              description: a list of fields to order by. Allowed values are 'estimated_hours', 'due_date', 'updated', 'created'
              required: false
              type: string
              paramType: query
            - name: search
              description: perform a wildcard search. Will search fields 'title'
              required: false
              type: string
              paramType: query
        """
        return super(TaskViewSet, self).list(request, *args, **kwargs)

# Serializers define the API representation.
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource        

# ViewSets define the view behavior.
class ResourceViewSet(viewsets.ModelViewSet):
    
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


# Serializers define the API representation.
class ProjectSerializer(serializers.ModelSerializer):

    task_set = TaskSerializer(many=True, read_only=True)
    resource_set = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Project  
        fields = ('title', 'description', 'start_date', 'end_date', 'is_billable', 'is_active', 'task_set', 'resource_set',)      


class ProjectFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(name="resource__user")

    class Meta:
        model = Project
        fields = ['is_billable', 'is_active', 'user',]

# ViewSets define the view behavior.
class ProjectViewSet(viewsets.ModelViewSet):
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_class = ProjectFilter
    search_fields = ('title', 'description')
    ordering_fields = ('start_date', 'end_date', 'title')

    # this is overwritten purely for the purpose of documentation for swagger
    def list(self, request, *args, **kwargs):
        """
        List available projects.
        ---
          parameters_strategy: merge
          parameters:
            - name: is_billable
              description: filter projects by is_billable (note needs to be True or False. Case matters)
              required: false
              type: boolean
              paramType: query
            - name: is_active
              description: filter projects by is_active (note needs to be True or False. Case matters)
              required: false
              type: boolean
              paramType: query
            - name: user
              description: filter projects by user_id
              required: false
              type: string
              paramType: query
            - name: ordering
              description: a list of fields to order by. Allowed values are start_date, end_date, title
              required: false
              type: string
              paramType: query
            - name: search
              description: perform a wildcard search. Will search fields title, description
              required: false
              type: string
              paramType: query
        """
        return super(ProjectViewSet, self).list(request, *args, **kwargs)
    

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



# Routers provide an easy way of automatically determining the URL conf.
project_router = routers.DefaultRouter()
project_router.register('projects', ProjectViewSet)
project_router.register('resources', ResourceViewSet)
project_router.register('tasks', TaskViewSet)