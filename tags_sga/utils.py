'''
Created on 10 mar. 2018

@author: luisza
'''
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from tags_sga.models import (SGAIndicator,
                              Category,
                              Pictogram
                              )


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def render_pdf_view(request, name,  template_path, context):
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"'%(name,)
    # find the template and render it.
    template = get_template(template_path)
    html = template.render( context)
    # create a pdf
    pisaStatus = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response




def get_label_component(components):
    indicators = SGAIndicator.objects.filter(component__in=components).distinct()
    warnigns_categories =  Category.objects.filter(sgaindicator__in=indicators)
    pictugram = Pictogram.objects.filter(category__in=warnigns_categories).order_by('-human_tag')
    return (indicators,warnigns_categories,pictugram)


def get_label_sustance(sustance):
    (indicators,warnigns_categories,pictugram)=get_label_component(sustance.componets.all())
    
    label = {# list of values kept on product label
    'sustance': sustance.marketing_name,
    'pictograms': pictugram,
    'components': sustance.componets,
    'warning_word': pictugram.first().get_human_tag(),
    'warning_prudences':"", #prudences
    'warning_tips':"", #prudences
    }
    return label
    
    