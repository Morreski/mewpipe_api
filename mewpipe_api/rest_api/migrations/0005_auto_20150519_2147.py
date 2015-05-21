# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_auto_20150519_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='watchers',
            field=models.ManyToManyField(related_name='watchers', through='rest_api.View', to='rest_api.User'),
        ),
    ]
