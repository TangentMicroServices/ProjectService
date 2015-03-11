from django.db import models
from datetime import date


class Project(models.Model):

    def __unicode__(self):
        return self.title 
    
    title = models.CharField(max_length=100)
    description = models.TextField()

    start_date = models.DateField('Start Date', blank=False, null=False)
    end_date = models.DateField('End Date', blank=True, null=True)
    is_billable = models.BooleanField('Is Billable', default=True)
    is_active = models.BooleanField('Is Active', default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def quick_create(title=None, description=None, user=None, start_date=None, is_billable=False, is_active=True):
        '''
        Utility method for quickly creating a an instance
        '''
        if title is None:
            title = "Lorum Ipsum"

        if description is None:
            description = "some description text .."

        if start_date is None:
            start_date = date.today()

        if user is None:
            user = 1        

        data = {
            "title": title, 
            "description": description,
            "start_date": start_date,
            #"user": user,
            "is_active": is_active,
            "is_billable": is_billable
        }

        return Project.objects.create(**data)

class Resource(models.Model):
    '''
    A user working on a project
    '''
    
    #def __unicode__(self):
    #    return "{0}: {1}" . format (self.project.title, self.rate)

    project = models.ForeignKey(Project)
    user = models.CharField(max_length=200, db_index=True)

    start_date = models.DateField('Start Date', blank=False, null=False)
    end_date = models.DateField('End Date', blank=True, null=True)
    
    rate = models.FloatField(default=0.00)
    agreed_hours_per_month = models.DecimalField('Agreed Hours Per Month', max_digits=5, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("project", "user")

    @staticmethod 
    def quick_create(project = None, user = 1, start_date = None, **kwargs):
        
        if project is None:
            project = Project.quick_create()

        if start_date is None:
            start_date = date.today()

        data = {
            "project": project, 
            "user": user, 
            "start_date": start_date
        }
        data.update(kwargs)

        return Resource.objects.create(**data)


class Task(models.Model):
    
    def __unicode__(self):
        return "%s: %s" % (self.project.title, self.title)

    project = models.ForeignKey(Project)
    title = models.CharField('Task Name', max_length=200, blank=False, null=False)
    
    due_date = models.DateField('Due Date', blank=True, null=True)
    estimated_hours = models.DecimalField('Est. Hours', max_digits=5, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def verbose_name(self):
        return "{0} - {1}" . format (self.project.name, self.name)
    
    class Meta:
        verbose_name = u"ProjectTask"
        verbose_name_plural = verbose_name

    @staticmethod
    def quick_create(project=None, title=None):
        '''
        Utility method for quickly creating a an instance
        '''
        if project is None:
            project = Project.quick_create()
        if title is None:
            title = "Do some work"

        data = {
            "project": project,
            "title": title,
        }

        return Task.objects.create(**data)
    