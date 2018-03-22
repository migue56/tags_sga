from django.contrib import admin
from .models import (
    Pictogram,
    Tip,
    Prudence,
    Category,
    SGAIndicator,
    Component,
    Sustance,
    Provider,
    )

from .utils import (render_pdf_view,
                    get_label_sustance)




def make_tag_pdf(modeladmin, request, queryset):
    for object in queryset:
         label= get_label_sustance(object)
         print (label)
         context ={'obj': object}
         return render_pdf_view(request, "etiqueta", 
                           'tags.html', context)
make_tag_pdf.short_description = "Download tag"
class SustanceAdmin(admin.ModelAdmin):
    actions = [make_tag_pdf]




admin.site.register(Sustance,SustanceAdmin) # sustance
admin.site.register(Component) # sustance


admin.site.register(Pictogram) # SGA Control
admin.site.register(Tip) # SGA Control
admin.site.register(Prudence) # SGA Control
admin.site.register(Category) # SGA Control
admin.site.register(SGAIndicator)
admin.site.register(Provider)