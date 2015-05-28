# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0006_auto_20150527_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail_frame',
            field=models.IntegerField(default=0),
        ),
    ]
