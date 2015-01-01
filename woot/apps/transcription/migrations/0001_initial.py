# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('distribution', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('id_token', models.CharField(max_length=8)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('char', models.CharField(default='', max_length=255, choices=[('nj', 'new job'), ('ea', 'ended audio'), ('p', 'previous'), ('n', 'next'), ('r', 'replay'), ('pp', 'play pause'), ('a', 'add new word'), ('c', 'copy down'), ('t', 'tick')])),
                ('audio_time', models.DecimalField(decimal_places=6, max_digits=8, null=True)),
                ('client', models.ForeignKey(related_name='actions', to='distribution.Client')),
                ('job', models.ForeignKey(related_name='actions', to='distribution.Job')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CSVFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('path', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('client', models.ForeignKey(related_name='csv_files', to='distribution.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grammar',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False)),
                ('is_processed', models.BooleanField(default=False)),
                ('id_token', models.CharField(max_length=8, null=True)),
                ('name', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_completed', models.DateTimeField(null=True)),
                ('language', models.CharField(default='english', max_length=255, choices=[('en', 'english'), ('es', 'spanish')])),
                ('complete_rel_file', models.FileField(upload_to='completed')),
                ('client', models.ForeignKey(related_name='grammars', to='distribution.Client')),
                ('project', models.ForeignKey(related_name='grammars', to='distribution.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('id_token', models.CharField(max_length=8)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('utterance', models.CharField(max_length=255)),
                ('time_to_complete', models.DecimalField(decimal_places=6, max_digits=8, null=True)),
                ('number_of_plays', models.IntegerField(default=0)),
                ('job', models.ForeignKey(related_name='revisions', to='distribution.Job')),
            ],
            options={
                'get_latest_by': 'date_created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transcription',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('id_token', models.CharField(max_length=8)),
                ('audio_file_data_path', models.CharField(max_length=255)),
                ('audio_file', models.FileField(upload_to='audio')),
                ('audio_time', models.DecimalField(decimal_places=6, max_digits=8, null=True)),
                ('audio_rms', models.CharField(max_length=255)),
                ('confidence', models.CharField(max_length=255)),
                ('utterance', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('confidence_value', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('requests', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_processed', models.BooleanField(default=False)),
                ('date_last_requested', models.DateTimeField(null=True)),
                ('client', models.ForeignKey(related_name='transcriptions', to='distribution.Client')),
                ('grammar', models.ForeignKey(related_name='transcriptions', to='transcription.Grammar')),
                ('job', models.ForeignKey(related_name='transcriptions', to='distribution.Job', null=True)),
                ('project', models.ForeignKey(related_name='transcriptions', to='distribution.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WavFile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('client', models.ForeignKey(related_name='wav_files', to='distribution.Client')),
                ('grammar', models.ForeignKey(related_name='wav_files', to='transcription.Grammar')),
                ('project', models.ForeignKey(related_name='wav_files', to='distribution.Project')),
                ('transcription', models.OneToOneField(related_name='wav_file', to='transcription.Transcription', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('id_token', models.CharField(max_length=8)),
                ('char', models.CharField(max_length=255)),
                ('unique', models.BooleanField(default=False)),
                ('tag', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RevisionWord',
            fields=[
                ('word_ptr', models.OneToOneField(to='transcription.Word', serialize=False, parent_link=True, auto_created=True, primary_key=True)),
                ('revision', models.ForeignKey(related_name='words', to='transcription.Revision')),
            ],
            options={
            },
            bases=('transcription.word',),
        ),
        migrations.AddField(
            model_name='word',
            name='client',
            field=models.ForeignKey(related_name='words', to='distribution.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='word',
            name='grammar',
            field=models.ForeignKey(related_name='words', to='transcription.Grammar'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='word',
            name='project',
            field=models.ForeignKey(related_name='words', to='distribution.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='word',
            name='transcription',
            field=models.ForeignKey(related_name='words', to='transcription.Transcription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='revision',
            name='transcription',
            field=models.ForeignKey(related_name='revisions', to='transcription.Transcription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='revision',
            name='user',
            field=models.ForeignKey(related_name='revisions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='csvfile',
            name='grammar',
            field=models.OneToOneField(related_name='csv_file', to='transcription.Grammar', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='csvfile',
            name='project',
            field=models.ForeignKey(related_name='csv_files', to='distribution.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='revision',
            field=models.ForeignKey(related_name='actions', to='transcription.Revision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='transcription',
            field=models.ForeignKey(related_name='actions', to='transcription.Transcription'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='user',
            field=models.ForeignKey(related_name='actions', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
