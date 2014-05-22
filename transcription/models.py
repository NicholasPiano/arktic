#django
from django.core.files import File

#local
from archive.models import Archive
from transcription.fields import AudioField
from transcription.base_model import Model

#util
import wave
import numpy
from subprocess import Popen, PIPE
from os.path import splitext, basename


#every time a set of transcriptions is requested, it is sent as a Job object.
class Job(Model):
    #properties
    user = models.ForeignKey() #user that requested the job

    #initialiser
    #instance methods

class Transcription(Model):
    #properties
    utterance = models.TextField(max_length=200)
    word_list = [] #used to sort transcription objects
    archive = models.ForeignKey(Archive) #one-to-many from archive-side (archive.transcription_set)
    user_dictionary = {} #list of users that have requested this transcription along information about their activity
    audiofile = models.OneToOneField(AudioFile, primary_key=True)

    #initialiser
    def __init__(self, filename):
        self.audiofile = AudioFile(filename) #also handles shuffling things between folders

    #instance methods


#holds audio file for transcription object
class AudioFile(File):

    #properties
    audiofile = AudioField()#actual sound file in memory
    #converted_audiofile = #only if file is not already .wav
    #waveform = #holds waveform to be displayed to the user

    #initialiser
    def __init__(self, filename):
        self.audiofile = File(filename)
        self.ext =
        self.waveform = WaveForm()

    #instance methods


    #holds JSON data about the shape of the waveform of the audio track
    class WaveForm(object):
        #properties
        waypoint_dictionary = {} #for each point on the x-axis

        #initialiser
        def __init__(self, audiofile):


        #instance methods
