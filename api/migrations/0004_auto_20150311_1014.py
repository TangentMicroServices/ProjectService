# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_resource_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='user',
            field=models.CharField(default=0, max_length=200, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('project', 'user')]),
        ),
    ]
