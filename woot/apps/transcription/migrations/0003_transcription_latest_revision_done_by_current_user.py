# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0002_auto_20150101_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='latest_revision_done_by_current_user',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
