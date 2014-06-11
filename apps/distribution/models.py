#distribution.models

#django
from django.db import models
from django.db.models.fields.files import FileField
from django.core.files import File

#local
from apps.users.models import User

#util
import json
import os

#class vars


class Client(models.Model):
    #connections

    #properties
    name = models.CharField(max_length=100)
    data_json = FileField(max_length=255, upload_to='json', editable=False, null=True)

    #instance methods
    def __unicode__(self):
        return self.name

    #delete
    def delete(self, *args, **kwargs):
        #archives
        for archive in self.archives.all():
            archive.delete() #call custom delete method

        super(Client, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Client, self).save(*args, **kwargs)
            self.create_data_json()
        else:
            self.data_json = File(open(self.name+'.json', 'w+'))
            super(Client, self).save(*args, **kwargs)
            self.create_data_json()

    def create_data_json(self):
        unique_words_list = []
        #store list of unique words in each transcription
        for transcription in self.transcriptions.all():
            unique_words_list.append(transcription.utterance)
            for word in transcription.words.all():
                if word.char not in unique_words_list:
                    unique_words_list.append(word.char)

        f = open(self.data_json.path, 'w+')
        f.write(json.dumps(unique_words_list))
        self.data_json = File(f)

    def update_data_json(self):
        pass

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
