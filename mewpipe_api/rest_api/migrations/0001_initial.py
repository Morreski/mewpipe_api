# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(unique=True, max_length=100, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=40, db_index=True)),
                ('author', models.ForeignKey(to='rest_api.User', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoTag',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
                ('tag_level', models.IntegerField(choices=[(0, b'Secondary'), (1, b'Primary')])),
                ('tag', models.ForeignKey(to='rest_api.Tag')),
                ('video', models.ForeignKey(to='rest_api.Video')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(to='rest_api.Tag', through='rest_api.VideoTag'),
        ),
        migrations.AddField(
            model_name='tag',
            name='videos',
            field=models.ManyToManyField(to='rest_api.Video', through='rest_api.VideoTag'),
        ),
    ]
