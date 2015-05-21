# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0009_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='html_body_template',
        ),
    ]
