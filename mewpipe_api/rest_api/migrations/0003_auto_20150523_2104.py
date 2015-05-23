# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0002_useraccount_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='buffer_share_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='buffer_view_count',
            field=models.IntegerField(default=0),
        ),
    ]
