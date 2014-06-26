#transcription.fields

#django
from django.db import models
from django.forms import forms
from django.utils.translation import ugettext_lazy as _

#local


#util


#class vars


#classes
class ContentTypeRestrictedFileField(models.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
        	content_type = file.content_type
        	if content_type not in self.content_types:
        		raise forms.ValidationError(_('Filetype not supported.'))
        except AttributeError:
	    	pass

        return data
