# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, verbose_name=b'Name', blank=True)),
                ('start_date', models.DateField(verbose_name=b'Start Date')),
                ('end_date', models.DateField(null=True, verbose_name=b'End Date', blank=True)),
                ('rate', models.FloatField(default=0.0)),
                ('agreed_hours_per_month', models.DecimalField(default=0, verbose_name=b'Agreed Hours Per Month', max_digits=5, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(to='api.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Task Name')),
                ('due_date', models.DateField(null=True, verbose_name=b'Due Date', blank=True)),
                ('estimated_hours', models.DecimalField(default=0, verbose_name=b'Est. Hours', max_digits=5, decimal_places=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(to='api.Project')),
            ],
            options={
                'verbose_name': 'ProjectTask',
                'verbose_name_plural': 'ProjectTask',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(default=datetime.date(2015, 2, 18), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateField(null=True, verbose_name=b'End Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name=b'Is Active'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='is_billable',
            field=models.BooleanField(default=True, verbose_name=b'Is Billable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.date(2015, 2, 18), verbose_name=b'Start Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(default=datetime.date(2015, 2, 18), auto_now=True),
            preserve_default=False,
        ),
    ]
