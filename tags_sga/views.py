from django.shortcuts import render
from django import forms
from django.http import HttpResponseForbidden, Http404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

from django.views.generic import ListView, CreateView

from .models import (
    Pictogram,
    Tip,
    Prudence,
    Category,
    SGAIndicator,
    Component,
    Sustance,
    )
from .utils import (render_pdf_view,
                    get_label_sustance)

from .form import SustanceForm

from django.views.decorators.http import require_http_methods


from django.views.generic import View


    
class CreateSustanceView(CreateView):
    template_name = 'sustance/sustance_form.html'
    form_class = SustanceForm
    model = Sustance
    success_url = 'sustance/'

    def form_valid(self, form):
        return super().form_valid(form)



        
class ListSustanceView(ListView):
    template_name = 'sustance/sustance_list.html'
    paginate_by = 25


    def get_context_data(self, **kwargs):
        context = super(ListSustanceView, self).get_context_data(**kwargs)
        context['object_list'] = self.queryset
        return context

    def get_queryset(self):
        self.queryset = Sustance.objects.all()

        return self.queryset
  
    
# ----------------------------------------
       
        

@login_required     
@require_http_methods(["GET", "POST"])
def Sustance_detail(request, sustance_pk):
    sustance_pk = ObjectId(sustance_pk)
    try:
        p = Sustance.objects.get({'_id':sustance_pk})
    except Sustance.DoesNotExist:
        raise Http404("Sustance does not exist")
    return render(request, 'sustance/sustance_detail.html', {'sustance': p})

def Sustance_delete(request, sustance_pk):
    sustance_pk = ObjectId(sustance_pk)
    try:
        p = Sustance.objects.get({'_id':sustance_pk})
        p.delete()
    except Sustance.DoesNotExist:
        raise Http404("Sustance does not exist")
    return render(request, 'sustance/sustance_detail.html', {'sustance': p})


@login_required     
@require_http_methods(["GET", "POST"])
def Sustance_pdf(request, sustance_pk):
    sustance_pk = ObjectId(sustance_pk)
    try:
         object = Sustance.objects.get({'_id':sustance_pk})
         label= get_label_sustance(object) 
         context ={'obj': label}
         return render_pdf_view(request, "etiqueta", 'tags/tag_packing.html', context)
    except Sustance.DoesNotExist:
        raise Http404("Sustance does not exist")
    return render(request, 'detail.html', {'sustance': p})


