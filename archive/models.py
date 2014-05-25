#django
from django.db import models
from django.core.files import File

#local
from arktic.settings import MEDIA_ROOT
from archive.fields import ContentTypeRestrictedFileField

#util
import os
import re
import zipfile as zp
import shutil as sh
import csv

#class vars
ARCHIVE_ROOT = os.path.join(MEDIA_ROOT, 'archive')

class Archive(models.Model):
    #properties
    file = ContentTypeRestrictedFileField(upload_to='archive', max_length=255, content_types=['application/zip'])
    relfile_delimiter = models.CharField(max_length=1) #only used the first time

    #save
    def save(self, *args, **kwargs):
        if self.pk is None: #if the archive is being uploaded for the first time
            super(Archive, self).save(*args, **kwargs)
            self.extract(*args, **kwargs)
        else:
            super(Archive, self).save(*args, **kwargs)

    def extract(self, *args, **kwargs):
        #1. extract zip
        self.file_list = []

        self.zip_file = zp.ZipFile(self.file.file)
        for name in self.zip_file.namelist():
            self.file_list.append(name)

        self.extract_tree, self.ext = os.path.splitext(self.zip_file.filename)
        self.extract_path = os.path.join(ARCHIVE_ROOT, self.extract_tree)
        self.zip_file.extractall(path=self.extract_path)

        #2. sort into relfile and audio files - first make relfile from each object, then validate.
        for file in self.file_list:
            if re.search(r'\w+\/$', file) is None: #matches trailing slash to weed out directories
                if re.search(r'.csv', file) is not None: #relfile
                    open_file = File(open(os.path.join(self.extract_path, file)))
                    (file_subpath, filename) = os.path.split(file) #path splitter os.path.split
                    self.relfiles.create(file=open_file, name=filename, relfile_delimiter=self.relfile_delimiter)

        #3. link relfiles and transcriptions
        big_transcription_dictionary = {}
        for relfile in self.relfiles.all():
            big_transcription_dictionary.update(relfile.transcription_dictionary)
        for audio_file in self.file_list:
            if audio_file in big_transcription_dictionary: #actually is an audio file
                kwargs = big_transcription_dictionary[audio_file]
                kwargs += {'audio_file':audio_file}
                self.transcriptions.create(**kwargs)

        #4. remove extract tree after use
        sh.rmtree(os.path.join(self.extract_path, self.extract_tree))

    #instance methods
    def __unicode__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        #delete actual zip files
        self.file.delete(save=False)

        #also delete files from relfiles/audio files, cos it wont happen in relfile.delete
        for relfile in self.relfiles.all():
            relfile.file.delete(save=False)

        super(Archive, self).delete(*args, **kwargs)


class RelFile(models.Model):
    #properties
    file = models.FileField(upload_to='relfile', max_length=255, editable=False) #switch to audiofield when ready
    name = models.CharField(max_length=100, editable=False)
    archive = models.ForeignKey(Archive, related_name='relfiles', editable=False)
    relfile_delimiter = models.CharField(max_length=1)
    transcription_dictionary = {}

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(RelFile, self).save(*args, **kwargs)
        #parse into audio file name list and create transcription objects
        #1. read lines
        lines = self.file.file.readlines()
        #2. for each lines, get audio_file name, utterance, any other information
        for line in lines:
#             line_split = line.split(self.relfile_delimiter)
            line_split = line.split('|')
            self.transcription_dictionary[line[0]] = {'column2':line_split[1], #grammar type?
                                                      'column3':line_split[2], #translation?
                                                      'utterance':line_split[3],
                                                      'column5':line_split[4], #boolean value?
                                                      'column6':line_split[5],} #some value?


    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super(RelFile, self).delete(*args, **kwargs)
