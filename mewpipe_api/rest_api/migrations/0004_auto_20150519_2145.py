# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_video_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rest_api.User')),
                ('ip', models.GenericIPAddressField(unpack_ipv4=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rest_api.user',),
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rest_api.User')),
            ],
            options={
                'abstract': False,
            },
            bases=('rest_api.user',),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
                ('counter', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to='rest_api.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='video',
            name='daily_view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='monthly_view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='total_view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='weekly_view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='video',
            name='yearly_view_cont',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='view',
            name='video',
            field=models.ForeignKey(to='rest_api.Video'),
        ),
        migrations.AddField(
            model_name='user',
            name='watched',
            field=models.ManyToManyField(to='rest_api.Video', through='rest_api.View'),
        ),
        migrations.AddField(
            model_name='video',
            name='watchers',
            field=models.ManyToManyField(related_name='watcher', through='rest_api.View', to='rest_api.User'),
        ),
    ]
