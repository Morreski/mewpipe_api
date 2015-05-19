# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_auto_20150519_2147'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='view',
            unique_together=set([('video', 'user')]),
        ),
    ]
