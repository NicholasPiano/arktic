#users.models

#django
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

#local

class Employee(models.Model):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('employee'))
