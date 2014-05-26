#django
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

#third party
from userena.models import UserenaBaseProfile

#local

class Employee(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('employee'))
