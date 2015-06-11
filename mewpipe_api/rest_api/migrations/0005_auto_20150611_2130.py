# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0004_useraccount_auth_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='username',
            field=models.CharField(max_length=50, verbose_name='Username'),
        ),
        migrations.AlterUniqueTogether(
            name='useraccount',
            unique_together=set([('username', 'auth_provider')]),
        ),
    ]
