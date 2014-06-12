#distribution.models

#django
from django.db import models
from django.db.models.fields.files import FileField
from django.core.files import File

#local
from apps.users.models import User
from arktic.settings import MEDIA_ROOT

#util
import os

#class vars


class Client(models.Model):
    #connections

    #properties
    name = models.CharField(max_length=100)

    #instance methods
    def __unicode__(self):
        return self.name

    #delete
    def delete(self, *args, **kwargs):
        #archives
        for archive in self.archives.all():
            archive.delete() #call custom delete method

        super(Client, self).delete(*args, **kwargs)

    def __init__(self, *args, **kwargs):
            super(Client, self).__init__(*args, **kwargs)
            self.create_autocomplete_words()

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
                for word in transcription.words.all():
                    if word.char not in current_word_list and word.char not in new_word_list:
                        new_word_list.append(word.char)

        #add one AutocompleteWord for each one.
        for word in new_word_list:
            self.words.create(char=word)


class Job(models.Model): #a group of 50 transcriptions given to a user.
    #connections
    client = models.ForeignKey(Client, related_name='jobs')
    user = models.ForeignKey(User, related_name='jobs')

    #properties
    is_active = models.BooleanField(default=True)
    total_transcription_time = models.DecimalField(max_digits=5, decimal_places=5, editable=False, default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)
    #-performance
    #-average confidence
    #-time taken
    #-types of transcription

    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Job, self).save(*args, **kwargs)
        else:
            super(Job, self).save(*args, **kwargs)
            self.get_transcription_set()

    def __unicode__(self):
        return ('Job ' + str(self.pk) + ': ' + self.user.user.username)

    def get_transcription_set(self):
        #get all transcriptions and sort them by utterance
        sorted_transcription_set = sorted(self.client.transcriptions.filter(requests=0), key=lambda x: x.utterance, reverse=False)
        transcription_set = sorted_transcription_set #however many remain
        if len(sorted_transcription_set) >= 50:
            transcription_set = sorted_transcription_set[:50] #first 50 transcriptions

        #add to job object
        for transcription in transcription_set:
            transcription.requests += 1
            self.transcriptions.add(transcription)

class AutocompleteWord(models.Model):
    client = models.ForeignKey(Client, related_name='words')
    char = models.CharField(max_length=100)
