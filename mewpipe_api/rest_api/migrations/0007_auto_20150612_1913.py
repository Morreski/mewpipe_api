# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0006_auto_20150612_1746'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='useraccount',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='useraccount',
            name='auth_provider',
        ),
    ]
