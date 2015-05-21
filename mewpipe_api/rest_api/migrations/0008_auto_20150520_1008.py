# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0007_auto_20150519_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='daily_share_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='monthly_share_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='total_share_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='weekly_share_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='yearly_share_cont',
            field=models.IntegerField(default=0),
        ),
    ]
