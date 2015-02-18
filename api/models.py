from django.db import models


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

class Resource(models.Model):
    '''
    A user working on a project
    '''
    
    project = models.ForeignKey(Project)

    start_date = models.DateField('Start Date', blank=False, null=False)
    end_date = models.DateField('End Date', blank=True, null=True)
    
    rate = models.FloatField(default=0.00)
    agreed_hours_per_month = models.DecimalField('Agreed Hours Per Month', max_digits=5, decimal_places=2, default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_summary(self, entries):

        hours = entries.filter(user=self.user).aggregate(Sum('hours')).get("hours__sum", 0)
        total_cost = float(hours) * float(self.rate)
        return {
            "hours" : hours,
            "total_cost" : total_cost,
        }

    def get_entries(self):
        return Entry.objects.filter(user=self.user, project=self.project)    

class Task(models.Model):
    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.name)

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
    def get_tasks(user):
        
        user_projects = Project.objects.filter(resource_project__user=user).values_list("id")
        return ProjectTask.objects.filter(project__in=user_projects)    
    