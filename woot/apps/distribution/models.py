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

#vars

#classes

#need to talk about clients and batches.
#-When is a batch finished?
#-Does a batch have a due date?
class Client(models.Model):
    #connections
    #sub: jobs
    #sub: AutocompleteWords

    #properties
    name = models.CharField(max_length=100)

    #instance methods
    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.create_autocomplete_words()
            super(Client, self).save(*args, **kwargs)
        else:
            super(Client, self).save(*args, **kwargs)
            self.create_autocomplete_words()
            self.save() #call again I guess

    def create_autocomplete_words(self):
        #get list of current words
        current_word_list = []
        for word in self.words.all():
            if word.char not in current_word_list:
                current_word_list.append(word.char)
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
            self.words.create(char=word)

class Project(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='projects')

    #properties
    name = models.CharField(max_length=255)

class Job(models.Model): #a group of 50 transcriptions given to a user.
    #connections
    client = models.ForeignKey(Client, related_name='jobs')
    project = models.ForeignKey(Project, related_name='jobs')
    user = models.ForeignKey(User, related_name='jobs')
    #sub: actions
    #sub: transcriptions

    #properties
    is_active = models.BooleanField(default=True)
    active_transcriptions = models.IntegerField(default=NUMBER_OF_TRANSCRIPTIONS_PER_JOB)
    total_transcription_time = models.DecimalField(max_digits=5, decimal_places=5, editable=False, default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)
    #-average confidence
    #-time taken

    def save(self, *args, **kwargs):
        if self.pk is not None:
            #get remaining transcriptions in the job
            active_transcriptions = 0
            for transcription in self.transcriptions.all():
                if transcription.is_active:
                    active_transcriptions += 1
            self.active_transcriptions = active_transcriptions
            if active_transcriptions == 0:
                self.is_active = False
            super(Job, self).save(*args, **kwargs)
        else:
            super(Job, self).save(*args, **kwargs)
            self.get_transcription_set()

    def __unicode__(self):
        return ('#' + str(self.pk) + ': ' + str(self.user) + ', ' + str(self.client))

    def get_transcription_set(self):
        #get all transcriptions and sort them by utterance
        sorted_transcription_set = sorted(self.project.transcriptions.filter(requests=0), key=lambda x: x.utterance, reverse=False)
        transcription_set = sorted_transcription_set #however many remain
        if len(sorted_transcription_set) >= NUMBER_OF_TRANSCRIPTIONS_PER_JOB:
            transcription_set = sorted_transcription_set[:NUMBER_OF_TRANSCRIPTIONS_PER_JOB] #first 50 transcriptions

        #add up time from transcriptions

        #add to job object
        for transcription in transcription_set:
            transcription.requests += 1
            #make date last requested equal to now
            self.transcriptions.add(transcription)

    def check_transcriptions(self): #check for completions and set is_active = False
        active_transcriptions = 0
        for transcription in self.transcriptions.all():
            if not transcription.revisions.all():
                active_transcriptions += 1

        self.active_transcriptions = active_transcriptions
        if self.active_transcriptions == 0:
            self.is_active = False
        self.save()

class Action(models.Model): #lawsuit
    #connections
    job = models.ForeignKey(Job, related_name='actions')
    user = models.ForeignKey(User, related_name='actions')

    #properties
    button_id = models.CharField(max_length=255)
    transcription_id = models.CharField(max_length=255)
    transcription_content = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'for job ' + str(self.job) + ' ' + self.button_id + ', ' + self.transcription_id + ', ' + str(self.date_created) #datetime, button_id, etc.

class AutocompleteWord(models.Model):
    client = models.ForeignKey(Client, related_name='words')
    char = models.CharField(max_length=100)

    def __unicode__(self):
        return '"' + self.char + '" for client "' + str(self.client) + '"'
