# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0007_video_thumbnail_frame'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='privacy_policy',
            field=models.IntegerField(default=0, choices=[(0, b'Public'), (1, b'Private link'), (2, b'Private')]),
        ),
    ]
