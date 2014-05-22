import wave
import numpy
from subprocess import Popen, PIPE
from os.path import splitext, basename

#convert to wav
def convert_to_wav(filename):
    #split into filename and extention
    (name, ext) = splitext(basename(filename))
    #subprocess
    convert = Popen(['ffmpeg','-i',filename, name+'.wav'])
    convert.wait()
    #relocate converted file

filename = 'deadmau5.mp3'

convert_to_wav(filename)

# equivalent to 'source arg1 arg2 | sink'
# source = Popen(['source', 'arg1', 'arg2'], stdout=PIPE)
# sink = Popen(['sink'], stdin=source.stdout)
# source.stdout.close()
# source.wait()
# sink.wait()
