#django
from django.core.files import File
from django.contrib.auth.models import User

#local
from archive.models import Archive
from transcription.fields import AudioField
from transcription.base_model import Model
from arktic.settings import MEDIA_ROOT

#third party


#util
import wave as wv
import numpy as np
import os
import subprocess as sp

#class vars
WAV_TYPE = 'wav'
ORIGINAL_AUDIO_ROOT = os.path.join(MEDIA_ROOT, 'original_audio')
WAV_ROOT = os.path.join(MEDIA_ROOT, WAV_TYPE)


'''
Every time a set of transcriptions is requested, it is sent as a Job object. The job serves a
wrapper for a number of associated transcription objects

'''
class Job(Model):
    #properties
    user = models.ForeignKey(User) #user that requested the job

    #initialiser
    #instance methods

    #meta
    class Meta:
        pass

class Transcription(Model):
    #properties
    utterance = models.CharField(max_length=200)
    client = models.CharField(max_length=200)
    word_list = [] #used to sort transcription objects
    archive = models.ForeignKey(Archive) #one-to-many from archive-side (archive.transcription_set)
    users = models.ManyToManyField(User) #not used until job pulls transcription
    log_dictionary = {} #stores each transcription action in terms of date, user and job id
    audiofile = models.OneToOneField(AudioFile, primary_key=True)

    #initialiser
    def __init__(self, utterance, client, filename):
        self.utterance = utterance
        self.client = client
        self.audiofile = AudioFile(filename) #also handles shuffling things between folders

    #instance methods

    #meta
    class Meta:
        pass


#holds audio file for transcription object
class AudioFile(File):

    #properties
    name = models.CharField(max_length=200)
    audiofile = AudioField()#actual sound file in memory
    converted_audiofile = AudioField()#only if file is not already .wav
    waveform = WaveForm()#holds waveform to be displayed to the user

    #initialiser
    def __init__(self, filename):
        #find extension - if not .wav, convert
        (self.name, self.file_type) = os.path.splitext(os.path.basename(filename)) #(file, ext)
        #file itself is only accessed if it is a .wav
        self.convert_to_wav_and_store()

    #instance methods
    def convert_to_wav_and_store(self):
        #audio files have been dumped in their original format in the media folder.
        #These files need to be accessed using media/original_audio/'name'.'ext',
        #then saved as media/wav/'name'.wav

        #if the file is already a .wav, simply pass and do the copy at the end.
        #paths
        original_path = os.path.join(ORIGINAL_AUDIO_ROOT, self.name + '.' + self.file_type)
        self.audiofile = AudioField(original_path)
        wav_name = self.name + '.' + WAV_TYPE
        wav_path = os.path.join(WAV_ROOT, wav_name)

        if self.file_type is not WAV_TYPE:
            #process
            arg_list = ['ffmpeg', '-i']
            arg_list.append(original_path)
            arg_list.append(wav_path)
            convert_thread = sp.Popen(arg_list)
            convert_thread.wait() #will continue when done
        else:
            os.rename(original_path, wav_path) #move file to wav directory
        self.converted_audiofile = AudioField(wav_path)

    def delete(*args, **kwargs):
        pass

    #holds JSON data about the shape of the waveform of the audio track
    class WaveForm(object):
        #properties
        waypoint_dictionary = {} #for each point on the x-axis

        #initialiser
        def __init__(self, filename):
            #open file and convert to JSON waveform data

        #instance methods

    #meta
    class Meta:
        pass


