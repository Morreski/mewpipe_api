# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0010_remove_mail_html_body_template'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='yearly_share_cont',
            new_name='yearly_share_count',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='yearly_view_cont',
            new_name='yearly_view_count',
        ),
    ]
