from fabric.api import lcd, local

def prepare_deployment():
    local('python manage.py test arktic')

def deploy():

    APPS = (
        'transcription',
    )

    for app in APPS:
        local('python manage.py migrate ' + app)
        local('python manage.py test ' + app)
