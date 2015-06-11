# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_auto_20150609_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='auth_provider',
            field=models.IntegerField(default=0, choices=[(0, b'Standard auth'), (0, b'Facebook auth')]),
        ),
    ]
