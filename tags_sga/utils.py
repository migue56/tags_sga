'''
Created on 10 mar. 2018

@author: luisza
'''
import os
import bson
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



def get_combinate_tips(tips,tips_list):
    #tips_list=[] # list with finaly tips
    tips_cleaning=[] # list with check and clean tips by combinations
    tips_exclude=[] # list with check and clean tips by combinations
    # Get tips with combinations and order by combinations count
    if tips: 
        tips_combinations=tips #._addSpecial( "$orderby", { 'combinations' : -1 } )
        for comb in  tips_combinations:
            list_comb=comb.combinations
            for ictips in list_comb:
                if ictips in tips:
                     tips_cleaning.append(ictips.pk)
                         
            if len(tips_cleaning) == len(list_comb):
                # remove child tips and add father tip
                for i in tips_cleaning: #exclude on results
                    tips_exclude.append(i)
                    
                if comb not in  tips_list: # adding the father tips
                     tips_list.append(comb)
            else:
                tips_cleaning.clear() 
        
        # list tips whitout combinations                
        for tip in tips:
            if tip not in  tips_list:
                if obj not in tips_exclude:
                    tips_list.append(tip)  
        
    return tips_list    

def get_combinate_prudence(prudence,prudence_list):
     for obj in  prudence:
        if obj not in prudence_list:
             prudence_list.append(obj)
     return prudence_list


   
def get_pictograms(pictogram,pictogram_list):
     for obj in  pictogram:
        if obj not in pictogram_list:
            pictogram_list.append(obj )
     return pictogram_list

def get_components_indictors(components):
    list_id=[]
    for isga in components:
        list_id.append(str(isga._id))
        
    return list_id


def get_label_component(components):
    tips_list=[] 
    pictogram_list=[]
    prudence_list=[]
    
    for isga in components:
            
        indicators = isga.sga_indicators
        for ind_class in indicators:
            warnigns_categories =  ind_class.warning_categories
            for warn_class in warnigns_categories:
                
                if warn_class.pictogram :
                     pictogram = warn_class.pictogram #.raw({ human_tag : -1}) #._addSpecial( "$orderby", { 'human_tag' : -1 } )
                     print (pictogram)
                else: pictogram=None     
                
                if warn_class.tips :
                     tips = warn_class.tips
                else: tips=None     
                    
                    
                if warn_class.prudence :
                     prudence = warn_class.prudence
                else: prudence=None     
                        
                # Processing data
                tips=get_combinate_tips(tips,tips_list)
                pictogram=get_pictograms(pictogram,pictogram_list)
                prudence=get_combinate_prudence(prudence,prudence_list)
      
        
    return (indicators,warnigns_categories,pictogram_list,tips_list,prudence_list)


def get_label_sustance(sustance):
    (indicators,warnigns_categories,pictogram,tips,prudence)=get_label_component(sustance.components)
    
    
    label = {# list of values kept on product label
    'sustance_code': sustance.cas_number,
    'sustance_name': sustance.marketing_name,
    'sustance_instructions': '',
    'provider': sustance.provider,
    'pictograms': pictogram,
    'pictograms_size': 150/ ( len(pictogram) if len(pictogram)>0 else 1 ),
    'components': sustance.components,
    'warning_word': pictogram[0].get_human_tag()  if len(pictogram)>0 else "",
    'warning_prudences':prudence, #prudences
    'warning_tips':tips, #prudences
    }
    return label
    
    