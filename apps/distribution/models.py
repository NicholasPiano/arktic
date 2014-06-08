#distribution.models

#django
from django.db import models

#local
from apps.users.models import User

#util

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

class Job(models.Model): #a group of 50 transcriptions given to a user.
    #connections
    user = models.ForeignKey(User, related_name='jobs')

    #properties
    client_id = models.CharField(max_length=100) #stores name of associated client.
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
        client = Client.objects.get(name=self.client_id)
        sorted_transcription_set = sorted(client.transcriptions.filter(requests=0), key=lambda x: x.utterance, reverse=False)
        transcription_set = sorted_transcription_set #however many remain
        if len(sorted_transcription_set) >= 50:
            transcription_set = sorted_transcription_set[:50] #first 50 transcriptions

        #add to job object
        for transcription in transcription_set:
            transcription.requests += 1
            transcription.users[self.user.user.username] += 1 #increment request dictionary
            self.transcriptions.add(transcription)
