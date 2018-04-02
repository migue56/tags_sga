
from django import forms
from django.contrib.admin import widgets
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from .models import (
    Pictogram,
    Tip,
    Prudence,
    Category,
    SGAIndicator,
    Component,
    Sustance,
    )

class SustanceForm(forms.Form):
    #id = forms.CharField(widget=forms.HiddenInput())
    marketing_name =  forms.CharField(max_length=250) 
    use_instructions = forms.CharField(max_length=500,widget=forms.Textarea )
#     components = forms.ModelMultipleChoiceField(
#         queryset=Component.objects.all(),
#         required=True,
#         widget=FilteredSelectMultiple(
#             verbose_name=_('Keywords Associated with Statement'),
#             is_stacked=False
#             )  
#     )    
    #    forms.MultipleChoiceField(
    #         widget=forms.widgets.CheckboxSelectMultiple(), 
    #         required=False)

    # provider = forms.ModelChoiceField(queryset=None)
    
    def build_field(self,updated_initial,initial_arguments ):
                   
        if hasattr(initial_arguments,"marketing_name"):
            updated_initial['marketing_name'] = initial_arguments.marketing_name
           
        if hasattr(initial_arguments,"use_instructions"):
            updated_initial['use_instructions'] = initial_arguments.use_instructions  
        
#         if hasattr(initial_arguments,"components"):            
#              updated_initial['components'] = [tag.marketing_name for tag in initial_arguments.components]
#           
    
    def __init__(self, *args, **kwargs):
            # Get 'initial' argument if any
            self.instance  = kwargs.get('initial', None)
            
            if self.instance :
                updated_initial = {}
                self.build_field(updated_initial,self.instance )
                kwargs.update(initial=updated_initial)
                
            super(SustanceForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.cleaned_data = self.instance if self.instance else None#super(SustanceForm, self).clean()
        if self.cleaned_data :
            marketing_name = self.cleaned_data.get('marketing_name')
            use_instructions = self.cleaned_data.get('use_instructions')
            #components = self.cleaned_data.get('components')
            if not marketing_name and not use_instructions :
                raise forms.ValidationError(_("Complete you the fields required"))
        return self.cleaned_data

    def is_valid(self):
         #valid = super(SustanceForm, self).is_valid()
         return self.clean()
    
    def save(self, commit=True):
        object = self.object if self.object else Sustance()
        object.marketing_name = self.cleaned_data['marketing_name']
        object.use_instructions = self.cleaned_data['use_instructions']
#       object.components = self.cleaned_data['components']

        #post.tags = Tag.objects(id__in=self.cleaned_data['tags'])
        if commit:
            object.save()

        return object
    
    
    
    


        

class ProviderForm(forms.Form):
    name = forms.CharField(max_length=250)
    phone = forms.CharField(max_length=30)
    address = forms.CharField(max_length=500)
    
    #components = fields.EmbeddedDocumentListField('Component')
    #provider = fields.EmbeddedDocumentListField('Provider')
    
    def clean(self):
        cleaned_data = super(ProviderForm, self).clean()
        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')
        address =cleaned_data.get('address')