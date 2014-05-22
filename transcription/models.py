#django
from django.db import models
from django.core.files import File

#local
from archive.models import Archive

#util
import wave
import numpy


#every time a set of transcriptions is requested, it is sent as a Job object.
class Job(models.Model):
    #properties
    user = #user that requested the job


    #initialiser
    #instance methods

class Transcription(models.Model):
    #properties
    utterance = models.TextField(max_length=200)
    word_list = [] #used to sort transcription objects
    archive = models.ForeignKey(Archive) #one-to-many from archive-side (archive.transcription_set)
    user_dictionary = {} #list of users that have requested this transcription along information about their activity
    audiofile = models.OneToOneField(AudioFile, primary_key=True)

    #initialiser
    def __init__(self, filename):
        #

    #instance methods


#holds audio file for transcription object
class AudioFile(File):

    #properties
    audiofile = #actual sound file in memory
    waveform = #holds waveform to be displayed to the user

    #initialiser
    def __init__(self, ):


    #instance methods


    #holds JSON data about the shape of the waveform of the audio track
    class WaveForm(object):
        #properties
        waypoint_dictionary = {} #for each point on the x-axis

        #initialiser
        def __init__(self, audiofile):


        #instance methods
