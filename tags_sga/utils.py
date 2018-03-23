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
                              Pictogram,
                              Tip,
                              Prudence
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



def get_combinate_tips(tips):
    tips_list=[]
    tips_cleaning=[]
    tips_combinations=Tip.objects.filter(combinations__in=tips).distinct()
    for comb in  tips_combinations:
        list_comb=comb.combinations.all()
        for ictips in list_comb:
            if ictips in tips:
                 tips_cleaning.append(ictips.pk)
                     
        if len(tips_cleaning) == len(list_comb):
            # remove child tips and add father tip
            tips=tips.exclude(id__in=tips_cleaning)
            tips_list.append(comb)
        else:
            tips_cleaning.clear() 
                
    for tip in tips:
        tips_list.append(tip)  
        
    return tips_list    

def get_label_component(components):

    indicators = SGAIndicator.objects.filter(component__in=components).distinct()
    warnigns_categories =  Category.objects.filter(sgaindicator__in=indicators)
    pictugram = Pictogram.objects.filter(category__in=warnigns_categories).order_by('-human_tag')
    tips = Tip.objects.filter(category__in=warnigns_categories).distinct()
    prudence = Prudence.objects.filter(category__in=warnigns_categories)
    
    tips=get_combinate_tips(tips)
      
        
    return (indicators,warnigns_categories,pictugram,tips,prudence)


def get_label_sustance(sustance):
    (indicators,warnigns_categories,pictugram,tips,prudence)=get_label_component(sustance.componets.all())
    
    label = {# list of values kept on product label
    'sustance': sustance.marketing_name,
    'pictograms': pictugram,
    'components': sustance.componets.all(),
    'warning_word': pictugram.first().get_human_tag(),
    'warning_prudences':prudence, #prudences
    'warning_tips':tips, #prudences
    }
    return label
    
    