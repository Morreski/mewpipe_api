# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0005_auto_20150525_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporaryuser',
            name='ip',
            field=models.GenericIPAddressField(unique=True, unpack_ipv4=True),
        ),
    ]
