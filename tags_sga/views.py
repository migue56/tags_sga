from django.shortcuts import render
from django import forms
from django.http import HttpResponseForbidden, Http404
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from pymodm.errors import ValidationError
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId


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


from django.views.decorators.http import require_http_methods

    
    
@login_required     
@require_http_methods(["GET", "POST"])
def Sustance_list(request):
    if request.method == 'POST':
        print("POST")
        
    elif request.method == 'GET':
        obj = Sustance.objects.all()
        print (obj.first())
        return render(request, 'index.html', {
             'object_list': obj,
             }, content_type='text/html; charset=utf-8')
        
    
        

@login_required     
@require_http_methods(["GET", "POST"])
def Sustance_detail(request, sustance_pk):
    sustance_pk = ObjectId(sustance_pk)
    try:
        p = Sustance.objects.get({'_id':sustance_pk})
        print (p)
    except Sustance.DoesNotExist:
        raise Http404("Sustance does not exist")
    return render(request, 'detail.html', {'sustance': p})


@login_required     
@require_http_methods(["GET", "POST"])
def Sustance_pdf(request, sustance_pk):
    sustance_pk = ObjectId(sustance_pk)
    try:
         object = Sustance.objects.get({'_id':sustance_pk})
         label= get_label_sustance(object) 
         context ={'obj': label}
         return render_pdf_view(request, "etiqueta", 'tag_packing.html', context)
    except Sustance.DoesNotExist:
        raise Http404("Sustance does not exist")
    return render(request, 'detail.html', {'sustance': p})


