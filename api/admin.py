from django.contrib import admin
from .models import Project, Resource, Task

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'start_date', 'end_date', 'is_billable', 'is_active', 'created')

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'start_date', 'end_date', 'rate', 'agreed_hours_per_month', 'created')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'title', 'due_date', 'estimated_hours', 'created')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Task, TaskAdmin)
