#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "woot.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

# from apps.transcription.models import Transcription, Revision;from apps.distribution.models import Action, Job, Project, CompletedProject;from apps.users.models import User
