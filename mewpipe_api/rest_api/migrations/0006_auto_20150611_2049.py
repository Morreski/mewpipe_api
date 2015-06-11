# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_auto_20150611_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='auth_provider',
            field=models.IntegerField(default=0, choices=[(0, b'Standard'), (1, b'Facebook')]),
        ),
    ]
