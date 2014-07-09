#from apps.transcription.models import Transcription, RelFile; T = Transcription.objects.all(); R = RelFile.objects.all(); from apps.users.models import User; u = User.objects.get(); from apps.distribution.models import Client, Project; client = Client.objects.get(); p = Project.objects.get();

#distribution.models

#django
from django.db import models
from django.db.models.fields.files import FileField
from django.core.files import File

#local
from apps.users.models import User
from settings.common import MEDIA_ROOT, NUMBER_OF_TRANSCRIPTIONS_PER_JOB

#util
import os
import zipfile as zp
import shutil as sh
import datetime as dt

#vars
COMPLETED_PROJECT_ROOT = os.path.join(MEDIA_ROOT, 'completed')

#classes
class Client(models.Model):
    #connections
    #sub: projects, jobs, archives, relfiles, transcriptions, autocomplete words

    #properties
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    #custom methods
    def create_autocomplete_words(self):
        #get list of current words
        current_word_list = []
        for word in self.words.all():
            if word.content not in current_word_list:
                current_word_list.append(word.content)
        #get all unique words and phrases from transcriptions
        new_word_list = []
        for transcription in self.transcriptions.all():
            if transcription.utterance not in current_word_list and transcription.utterance not in new_word_list:
                new_word_list.append(transcription.utterance)
                for word in transcription.utterance.split():
                    if word not in current_word_list and word not in new_word_list:
                        new_word_list.append(word)

        #add one AutocompleteWord for each one.
        for word in new_word_list:
            self.words.create(content=word)

    def update(self):
        for project in self.projects.filter(is_active=False):
            project.export()
            project.save()

class Project(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='projects')
    #sub: jobs, archives, relfiles, transcriptions

    #properties
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.client) + ' ' + self.name

    #custom methods
    def update(self):
        if self.transcriptions.filter(is_active=True).count()==0:
            if self.is_active:
                self.is_active = False

    def export(self):
        #create directory with name of project
        os.makedirs(os.path.join(COMPLETED_PROJECT_ROOT, self.name + '_completed'))

        for relfile in self.relfiles.all():
            #open relfile and get contents
            lines = relfile.file.file.readlines()
            #open new file in completed directory
            #new filename with '.out.csv'
            with open(os.path.join(os.path.join(COMPLETED_PROJECT_ROOT, self.name + '_completed'), os.path.splitext(relfile.name)[0]+'.out.csv'), 'w+') as complete_relfile:
                new_lines = []
                for line_number, line in enumerate(lines):
                    #find transcription by specifying line_number and grammar name
                    tokens = line.split('|')
                    grammar = os.path.splitext(os.path.basename(tokens[1]))[0]
                    print([grammar, line_number])
                    transcription = self.transcriptions.get(line_number=line_number, grammar=grammar) #should exist if the reverse worked
                    latest_revision = transcription.revisions.latest() #must exist
                    tokens[3] = latest_revision.utterance
                    new_line = '|'.join(tokens)
                    new_lines.append(new_line)
                for new_line in new_lines:
                    complete_relfile.write(new_line)
                self.completed_relfiles.create(client=self.client, archive=relfile.archive, relfile=relfile, file=File(complete_relfile), name=relfile.name)

        #zip directory
        zip_file = zp.ZipFile(os.path.join(COMPLETED_PROJECT_ROOT, self.name + '_completed.zip'), 'w', zp.ZIP_DEFLATED)
        for f in self.completed_relfiles.all():
            file_path = f.file.file.name
            zip_file.write(file_path, os.path.relpath(file_path, COMPLETED_PROJECT_ROOT))

        completed_project = self.client.completed_projects.create(name=self.name)

        completed_project.file.name = os.path.join('completed', self.name + '_completed.zip')
        completed_project.save()

        zip_file.close()

        #remove tree
        sh.rmtree(os.path.join(COMPLETED_PROJECT_ROOT, self.name + '_completed'))

class CompletedProject(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='completed_projects')

    #properties
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='completed', null=True, max_length=255)

    def __unicode__(self):
        return self.name + '_completed'

class Job(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='jobs')
    project = models.ForeignKey(Project, related_name='jobs')
    user = models.ForeignKey(User, related_name='jobs')
    #sub: transcriptions (null)

    #properties
    is_active = models.BooleanField(default=True)
    active_transcriptions = models.IntegerField(editable=False)
    total_transcription_time = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    time_taken = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, editable=False)

    def __unicode__(self):
        return str(self.project) + ' > #' + str(self.pk) + ': ' + str(self.user)

    #custom methods
    def get_transcription_set(self):
        transcriptions = self.project.transcriptions.filter(requests=0)
        sorted_transcription_set = sorted(transcriptions, key=lambda x: x.utterance, reverse=False)

        transcription_set = sorted_transcription_set #however many remain
        if len(sorted_transcription_set) >= self.active_transcriptions:
            transcription_set = sorted_transcription_set[:self.active_transcriptions] #first 50 transcriptions

        for transcription in transcription_set:
            transcription.requests += 1
            #make date last requested equal to now
            transcription.date_last_requested = dt.datetime.now()
            transcription.save()
            self.transcriptions.add(transcription)

    def update(self):
        self.active_transcriptions = self.transcriptions.filter(is_active=True).count()
        if self.active_transcriptions==0:
            if self.is_active:
                self.is_active = False

class Action(models.Model):
    #connections
    job = models.ForeignKey(Job, related_name='actions')
    user = models.ForeignKey(User, related_name='actions')

    #properties
    button_id = models.CharField(max_length=100)
    transcription_id = models.CharField(max_length=100)
    transcription_utterance = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'job: ' + str(self.job) + ' > "' + self.button_id + '" doing ' + self.transcription_id + ' ' + str(self.date_created)

    #custom methods

class AutocompleteWord(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='words')

    #properties
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return self.content
