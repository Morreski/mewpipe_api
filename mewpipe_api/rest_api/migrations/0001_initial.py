# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import rest_api.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
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
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=40, db_index=True)),
                ('description', models.TextField(blank=True)),
                ('privacy_policy', models.IntegerField(default=0, choices=[(0, b'Public'), (1, b'Private link'), (2, b'Private')])),
                ('thumbnail_frame', models.IntegerField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('total_view_count', models.IntegerField(default=0)),
                ('daily_view_count', models.IntegerField(default=0)),
                ('weekly_view_count', models.IntegerField(default=0)),
                ('monthly_view_count', models.IntegerField(default=0)),
                ('yearly_view_count', models.IntegerField(default=0)),
                ('total_share_count', models.IntegerField(default=0)),
                ('daily_share_count', models.IntegerField(default=0)),
                ('weekly_share_count', models.IntegerField(default=0)),
                ('monthly_share_count', models.IntegerField(default=0)),
                ('yearly_share_count', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0, choices=[(0, b'New'), (1, b'Uploading'), (2, b'Uploaded'), (3, b'Ready')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VideoTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
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
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('edition_date', models.DateTimeField(auto_now=True)),
                ('counter', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rest_api.User')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=50, verbose_name='Username')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='Email address')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name', blank=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Join date')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=('rest_api.user', models.Model),
            managers=[
                ('objects', rest_api.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryUser',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='rest_api.User')),
                ('ip', models.GenericIPAddressField(unique=True, unpack_ipv4=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('rest_api.user',),
        ),
        migrations.AddField(
            model_name='view',
            name='user',
            field=models.ForeignKey(to='rest_api.User'),
        ),
        migrations.AddField(
            model_name='view',
            name='video',
            field=models.ForeignKey(to='rest_api.Video'),
        ),
        migrations.AddField(
            model_name='video',
            name='author',
            field=models.ForeignKey(to='rest_api.User', null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(to='rest_api.Tag', through='rest_api.VideoTag'),
        ),
        migrations.AddField(
            model_name='video',
            name='watchers',
            field=models.ManyToManyField(related_name='watchers', through='rest_api.View', to='rest_api.User'),
        ),
        migrations.AddField(
            model_name='user',
            name='watched',
            field=models.ManyToManyField(to='rest_api.Video', through='rest_api.View'),
        ),
        migrations.AddField(
            model_name='tag',
            name='videos',
            field=models.ManyToManyField(to='rest_api.Video', through='rest_api.VideoTag'),
        ),
        migrations.AlterUniqueTogether(
            name='view',
            unique_together=set([('video', 'user')]),
        ),
    ]
