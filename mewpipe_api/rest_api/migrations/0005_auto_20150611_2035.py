# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_auto_20150611_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='auth_provider',
            field=models.PositiveIntegerField(default=0, blank=True, verbose_name='Provider', choices=[(0, b'Standard'), (1, b'Facebook')]),
        ),
    ]
