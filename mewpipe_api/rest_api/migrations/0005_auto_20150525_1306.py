# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_auto_20150525_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='last_login',
            field=models.DateTimeField(null=True),
        ),
    ]
