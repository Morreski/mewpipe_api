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
            field=models.PositiveIntegerField(default=0, verbose_name='Provider', choices=[(0, b'Standard'), (1, b'Facebook')]),
        ),
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
