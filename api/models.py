from django.db import models


class Project(models.Model):

    def __unicode__(self):
        return self.title 
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    