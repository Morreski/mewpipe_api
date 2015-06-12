# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_auto_20150611_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='username',
            field=models.CharField(unique=True, max_length=50, verbose_name='Username'),
        ),
    ]
