#libs.util

#django
from django.conf import settings

#local

#util
import string
import random
import wave
import audioop
import os
from subprocess import call

#vars
chars = string.ascii_uppercase + string.digits

def generate_id_token(Obj): #expects Obj.objects
  def get_id_token():
    return ''.join([random.choice(chars) for _ in range(8)]) #8 character string

  id_token = get_id_token()
  while Obj.objects.filter(id_token=id_token).count()>0:
    id_token = get_id_token()

  return id_token

''' AUDIO CONVERSION AND PROCESSING '''

### BRIEF DECRIPTION ###
# analyse a wav file (A-law compression, 8-bit sample width).

### INSTRUCTIONS ###
# - The main() function shown here demonstrates the code.
#   Copy it to your own project.

### REQUIREMENTS ###
# - tested with python 2.7.9 on Mac OS X 10.6.8
# - uses ffmpeg
# -- tested with ffmpeg version 2.5.1 (built with gcc 4.2.1)
# - uses python built-in modules:
# -- wave
# -- audioop
# -- subprocess

### DESCRIPTION ###
# 1] Use ffmpeg to convert A-law wav file to Microsoft PCM 16-bit wav file.
# 2] Use wave to read basic properties of the resulting wav file.
#    Calculate the total playing time in s of the wav file.
# 3] Read the wav file as 100 sections. Use audioop to find the
#    rms (root mean square) value of each section.
#    The rms is a good measure of the intensity of an audio section.
# 4] The getWAVFileProperties() function returns a tuple containing
#    - the total play time of the wav file in seconds
#    - a list of the rms values of each section.

### CONTROLS ###
sampleWidth = 2 # number of bytes in a frame.
  # for microsoft 16-bit PCM wav, this is 2.

def process_audio(input_path):
  # convert a-law wav file to microsoft pcm wav file
  cmd = ['ffmpeg','-y','-i',input_path,'-f','wav',input_path]
  call(cmd)

  # get properties of the pcm wav file
  seconds, rmsValues = getWAVFileProperties(input_path)

  return (seconds, rmsValues)

def getWAVFileProperties(filePath):

  a = wave.open(filePath, 'r')
  nFrames = a.getnframes()
  framerate = a.getframerate()
  seconds = nFrames / float(framerate)

  # get rms value for each section of the audio
  framesPerSection = int(nFrames / float(settings.NUMBER_OF_AUDIO_FILE_BINS)) # note the truncation
  rmsValues = []
  count = 0
  for i in range(settings.NUMBER_OF_AUDIO_FILE_BINS-1):
    section = a.readframes(framesPerSection)
    count += framesPerSection
    r = audioop.rms(section, sampleWidth)
    rmsValues.append(r)

  # all the truncated time adds up.
  # we therefore read the last audio section to the end of the file,
  # rather than to an integer number of frames.
  last = nFrames - count
  section = a.readframes(last)
  r = audioop.rms(section, sampleWidth)
  rmsValues.append(r)

  return seconds, rmsValues
