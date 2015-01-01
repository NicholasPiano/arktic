# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transcription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transcription',
            name='is_available',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transcription',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
