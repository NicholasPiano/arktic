#distribution.tests

#django
from django.test import TestCase

#local
from apps.transcription.models import Transcription, RelFile
from apps.distribution.models import Client, Project
from apps.users.models import User

#vars

#classes
class TestProjectExport(TestCase):

    def test(self):
        test_client = Client.objects.get(name='test')
        test_project = test_client.projects.get()
        test_relfile = test_project.relfiles.get()

        transcriptions = test_project.transcriptions.all()
        test_user = User.objects.get(email='nicholas.d.piano@gmail.com')

        #add revisions to each transcription object
        for transcription in transcriptions:
            transcription.revisions.create(user=test_user, utterance=transcription.pk)
            transcription.update()
            transcription.save()

        #update relfile
        test_relfile.update()
        test_relfile.save()

        #update project
        test_project.update()
        test_project.save()

        #update client
        test_client.update()
        test_client.save()

        #get completed project
        test_completed_project = test_client.completed_projects.get()
        self.assertEqual(test_completed_project.file.file.path!='', True) #contains some path
