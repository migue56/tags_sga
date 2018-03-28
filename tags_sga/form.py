
from django.db import models
from django import forms


class SustanceForm(forms.Form):
    marketing_name =  models.CharField(max_length=250) 
    #components = fields.EmbeddedDocumentListField('Component')
    use_instructions = models.CharField(max_length=500)
    #provider = fields.EmbeddedDocumentListField('Provider')