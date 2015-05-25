# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_auto_20150523_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='buffer_share_count',
        ),
        migrations.RemoveField(
            model_name='video',
            name='buffer_view_count',
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='birth_date',
            field=models.DateTimeField(null=True),
        ),
    ]
