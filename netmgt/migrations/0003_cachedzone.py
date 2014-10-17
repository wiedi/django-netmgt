# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netmgt', '0002_auto_20141017_0914'),
    ]

    operations = [
        migrations.CreateModel(
            name='CachedZone',
            fields=[
                ('key', models.CharField(max_length=250, unique=True, serialize=False, primary_key=True)),
                ('tag', models.CharField(max_length=250)),
                ('value', models.TextField(max_length=250)),
                ('updated', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
