# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0008_auto_20150520_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('body_template', models.TextField()),
                ('html_body_template', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
