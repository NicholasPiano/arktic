from django.db import models
from django.core.files import File
from archive.models import Archive


#every time a set of transcriptions is requested, it is sent as a Job object.
class Job(models.Model):
    #properties
    user =


    #initialiser
    #instance methods

class Transcription(models.Model):
    #general properties
    utterance = models.TextField(max_length=200)
    word_list = []
    archive = models.ForeignKey(Archive)
    user_dictionary = {} #list of users that have requested this transcription along information about their activity

    #initialiser
    def __init__(self):
        pass

    #instance methods
    #1. get waveform
    def get_waveform(self):


#holds audio file for transcription object
class AudioFile(File):

    #properties
    waveform = #holds waveform to be displayed to the user

    #initialiser
    #instance methods

    #holds JSON data about the shape of the waveform of the audio track
    class WaveForm(object):

