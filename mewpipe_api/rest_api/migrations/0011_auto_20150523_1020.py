# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import rest_api.models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0010_remove_mail_html_body_template'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='useraccount',
            managers=[
                ('objects', rest_api.models.CustomUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='useraccount',
            name='birth_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 23, 10, 19, 41, 240362, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='email',
            field=models.CharField(default='test@test.fr', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='first_name',
            field=models.CharField(default='firstname', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 23, 10, 20, 5, 682009, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useraccount',
            name='last_name',
            field=models.CharField(default='lastname', max_length=100),
            preserve_default=False,
        ),
    ]
