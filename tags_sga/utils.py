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

def get_list_components_tips(components):
    tips_list=[]
    for isga in components:
        indicators = isga.sga_indicators
        for ind_class in indicators:
            for it in ind_class.tips:
                 tips_list.append(it)
    return tips_list  
      
def get_list_components_prudences(components):
    tips_list=[]
    for isga in components:
        indicators = isga.sga_indicators
        for ind_class in indicators:
                for icatg in ind_class.warning_categories:
                    for iprudence in icatg.prudence:
                         tips_list.append(iprudence)
    return tips_list  

def  get_Orderby_Combinations(obj):
    return obj.combinations

"""
  tips: Are the indcators tips list
  tips_list: Array result
  warn_class: Class checking to filters tips var
  
"""
def get_combinate_tips(tips,tips_list,warn_class):
    #tips_list=[] # list with finaly tips
    tips_cleaning=[] # list with check and clean tips by combinations
    tips_exclude=[] # list with check and clean tips by combinations
    # Get tips with combinations and order by combinations count
    if tips:        
        tips_combinations=warn_class.tips  # tips of warn class
        sorted(tips_combinations, key=get_Orderby_Combinations,  reverse=True) 
    
        for comb in  tips_combinations:
            list_comb=comb.combinations # get list of combinations
            if list_comb:
                for ictips in list_comb:
                    if ictips in tips:
                         tips_cleaning.append(ictips._id)
                if len(tips_cleaning) == len(list_comb):
                    # remove child tips and add father tip                    
                    if comb not in  tips_list: # adding the father tips
                        tips_list.append(comb)
                    
                    for iclen in tips_cleaning: # adding cancelation of children tips
                             tips_exclude.append(iclen)
                             
                else:
                    tips_cleaning.clear() 
        
        # list tips whitout combinations                
        for tip in tips:
            if tip not in  tips_list and tip._id not in tips_exclude:  # no have been listed s  
                    tips_list.append(tip)  
                    
    sorted(tips_list, key=get_Orderby_Combinations,  reverse=True)    
    return tips_list    

""" Math the list of prudences by class warning and it math with the list of prudences 
on Indicator classes 
    warn_class_conten: List of warnigs class on Sustance Content
    warn_class_prudences: List of prudence by Indicaror SGA
"""
def get_match_content_and_category_produce(warn_class_conten,warn_class_prudences):
    prudence_combinations=[]
    for icontent_class in warn_class_conten:
        if icontent_class in warn_class_prudences:
            if ipr not in prudence_combinations:
                 prudence_combinations.append(ipr)
                 print (ipr)
"""
 Bind list of produce with combinations and remove prudence on combinations list
 prudence: List of prudences of indicator class
 prudence_list: Array / list to save results
 warn_class: List of class of content
"""
def get_combinate_prudence(prudence,prudence_list,warn_class):
    #prudence_list=[] # list with finaly prudence
    prudence_cleaning=[] # list with check and clean prudence by combinations
    prudence_exclude=[] # list with check and clean prudence by combinations
    prudence_combinations=[]
    # Get prudence with combinations and order by combinations count
    if prudence:        
      
        prudence_combinations=get_match_content_and_category_produce(prudence,warn_class)
        print (prudence_combinations)
        #prudence_combinations=warn_class.prudence  # prudence of warn class
        if prudence_combinations:
            sorted(prudence_combinations, key=get_Orderby_Combinations,  reverse=True) 
            for comb in  prudence_combinations:
                list_comb=comb.combinations # get list of combinations
                if list_comb:
                    for icprudence in list_comb:
                        if icprudence in prudence:
                             prudence_cleaning.append(icprudence._id)
                    if len(prudence_cleaning) == len(list_comb):
                        # remove child prudence and add father tip                    
                        if comb not in  prudence_list: # adding the father prudence
                            prudence_list.append(comb)
                        
                        for iclen in prudence_cleaning: # adding cancelation of children prudence
                                 prudence_exclude.append(iclen)
                                 
                    else:
                        prudence_cleaning.clear() 
        
        # list prudence whitout combinations                
            for tip in prudence:
                if tip not in  prudence_list and tip._id not in prudence_exclude:  # no have been listed s  
                        prudence_list.append(tip)  
                    
        sorted(prudence_list, key=get_Orderby_Combinations,  reverse=True)    
    return prudence_list  

# def get_combinate_prudence(prudence,prudence_list):
#      for obj in  prudence:
#         if obj not in prudence_list:
#              prudence_list.append(obj)
#      return prudence_list


def get_Orderby_human_tag(obj):
    return obj.human_tag   

def get_pictograms(pictogram,pictogram_list):
    sorted(pictogram, key=get_Orderby_human_tag,  reverse=True)
    for obj in  pictogram:
        if obj not in pictogram_list:
            pictogram_list.append(obj )

    sorted(pictogram_list, key=get_Orderby_human_tag,  reverse=True)            
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
    
    
    tips_list_ob=get_list_components_tips(components) # list all components tips 
    prudence_list_ob=get_list_components_prudences(components) # list all components categories 
    
    for isga in components:
        indicators = isga.sga_indicators
        for ind_class in indicators: # check class indicator
            warnigns_categories =  ind_class.warning_categories
            for warn_class in warnigns_categories:  #check list of class
                                    
                if warn_class.pictogram : # get pictograms of class
                     pictogram = warn_class.pictogram 
                else: pictogram=None         
                      
                get_combinate_tips(tips_list_ob,tips_list,warn_class)  # check tips on class
                
                get_combinate_prudence(prudence_list_ob,prudence_list,isga.warning_classes)
                
                pictogram=get_pictograms(pictogram,pictogram_list)
             
    return (indicators,warnigns_categories,pictogram_list,tips_list,prudence_list)


def get_label_sustance(sustance):
    (indicators,warnigns_categories,pictogram,tips,prudence)=get_label_component(sustance.components)
     
    label = {# list of values kept on product label
    'sustance_code': '',
    'sustance_name': sustance.marketing_name,
    'sustance_instructions': '',
    'provider': sustance.provider,
    'pictograms': pictogram,
    'pictograms_size': 150/ ( len(pictogram) if len(pictogram)>0 else 1 ),
    'components': sustance.components,
    'warning_word': pictogram[0].get_human_tag()  if len(pictogram)>0 else "",
    'warning_tips':tips, #prudences
    }
    return label
    
    