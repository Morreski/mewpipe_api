# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0007_auto_20150612_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='fb_uid',
            field=models.CharField(max_length=50, verbose_name='Uid Facebook', blank=True),
        ),
    ]
