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
                              Prudence,
                              Product
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
    tips_list=[] # list with finaly tips
    tips_cleaning=[] # list with check and clean tips by combinations
    # Get tips with combinations and order by combinations count
    if tips: 
        tips_combinations=tips._addSpecial( "$orderby", { 'combinations' : -1 } )
        for comb in  tips_combinations:
            list_comb=comb.combinations.all()
            for ictips in list_comb:
                if ictips in tips:
                     tips_cleaning.append(ictips.pk)
                         
            if len(tips_cleaning) == len(list_comb):
                # remove child tips and add father tip
                tips=tips.exclude(id__in=tips_cleaning)
                if comb not in  tips_list:
                     tips_list.append(comb)
            else:
                tips_cleaning.clear() 
        
        # list tips whitout combinations                
        for tip in tips:
            if tip not in  tips_list:
                tips_list.append(tip)  
        
    return tips_list    

def get_combinate_prudence(prudence):
    prudence_list=[]
    if prudence:
        return prudence
    
    return prudence_list


   
def get_pictograms(pictogram):
    pictogram_list=[]
    if pictogram:
        return pictogram
    
    return pictogram_list

def get_label_component(components):

    indicators = SGAIndicator.objects.raw({'component': { '$in': components} })
    warnigns_categories =  Category.objects.raw( { 'sgaindicator': { '$in': indicators}} )
    
    if not warnigns_categories :
         pictogram = warnigns_categories.pictogram._addSpecial( "$orderby", { 'human_tag' : -1 } )
    else: pictogram=None     
    
    if not warnigns_categories :
         tips = warnigns_categories.tip
    else: tips=None     
        
        
    if not warnigns_categories :
         prudence = warnigns_categories.prudence
    else: prudence=None     
            
    # Processing data
    tips=get_combinate_tips(tips)
    pictogram=get_pictograms(pictogram)
    prudence=get_combinate_prudence(prudence)
      
        
    return (indicators,warnigns_categories,pictogram,tips,prudence)


def get_label_sustance(sustance):
    (indicators,warnigns_categories,pictogram,tips,prudence)=get_label_component(sustance.componets)
    
    
    label = {# list of values kept on product label
    'sustance_code': sustance.cas_number,
    'sustance_name': sustance.marketing_name,
    'sustance_instructions': '',
    'provider': sustance.provider,
    'pictograms': pictogram,
    'pictograms_size': 150/ ( len(pictogram) if len(pictogram)>0 else 1 ),
    'components': sustance.componets,
    'warning_word': pictogram.first().get_human_tag()  if len(pictogram)>0 else "",
    'warning_prudences':prudence, #prudences
    'warning_tips':tips, #prudences
    }
    return label
    
    