# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0006_auto_20150519_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view',
            name='counter',
            field=models.IntegerField(default=1),
        ),
    ]
