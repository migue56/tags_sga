from tags_sga.utils import get_label_sustance
from django import template
from django.template.loader import render_to_string

from tags_sga.models import (
    Pictogram,
    Tip,
    Prudence,
    Category,
    SGAIndicator,
    Component,
    Sustance,
    )

register = template.Library()
register_tag = register.assignment_tag if hasattr(register, 'assignment_tag') else register.simple_tag

@register_tag
def get_general_label(sus_pk):
    obj = Sustance.objects.get({'_id':sus_pk})
    values = get_label_sustance(obj)
    
    
    value_body = render_to_string('tags/tag_packing.html', { 'obj': values })

    return value_body