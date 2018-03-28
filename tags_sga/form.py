
from django import forms


class SustanceForm(forms.Form):
    marketing_name =  forms.CharField(max_length=250) 
    use_instructions = forms.CharField(max_length=500)
    
    #components = fields.EmbeddedDocumentListField('Component')
    #provider = fields.EmbeddedDocumentListField('Provider')
  
    def build_field(self,updated_initial,initial_arguments ):    
        if initial_arguments.marketing_name:
            updated_initial['marketing_name'] = initial_arguments.marketing_name
            
        if initial_arguments.use_instructions:
            updated_initial['use_instructions'] = initial_arguments.use_instructions            
    
    def __init__(self, *args, **kwargs):
            # Get 'initial' argument if any
            initial_arguments = kwargs.get('initial', None)
            if initial_arguments:
                updated_initial = {}
                self.build_field(updated_initial,initial_arguments)
                kwargs.update(initial=updated_initial)
            super(SustanceForm, self).__init__(*args, **kwargs)

    def form_valid(self, form):


        return super().form_valid(form)
          
    def clean(self):
        cleaned_data = super(SustanceForm, self).clean()
        name = cleaned_data.get('marketing_name')
        email = cleaned_data.get('use_instructions')






        

class ProviderForm(forms.Form):
    name = forms.CharField(max_length=250)
    phone = forms.CharField(max_length=30)
    address = forms.CharField(max_length=500)
    
    #components = fields.EmbeddedDocumentListField('Component')
    #provider = fields.EmbeddedDocumentListField('Provider')
    
    def clean(self):
        cleaned_data = super(SustanceForm, self).clean()
        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')
        address =cleaned_data.get('address')