# This file contains the WSGI configuration required to serve up your
# web application at http://arkaeologic.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.

# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
activate_this = '/home/arkaeologic/.virtualenvs/arktic.com/bin/activate_this.py'
with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

import os
import sys

path = '/home/arkaeologic/arktic/'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'woot.settings.prod'
os.environ['DB_PWD'] = 'uqnhs77f'

import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
