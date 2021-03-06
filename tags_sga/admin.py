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
    Product,
    )

from .utils import (render_pdf_view,
                    get_label_sustance)




def make_tag_pdf(modeladmin, request, queryset):
    for object in queryset:
         label= get_label_sustance(object)
         print (label)
         context ={'obj': label}
         return render_pdf_view(request, "etiqueta", 
                           'tags.html', context)
make_tag_pdf.short_description = "Download genenic label"


def make_tag_packing_pdf(modeladmin, request, queryset):
    for object in queryset:
         label= get_label_sustance(object)
         print (label)
         context ={'obj': label}
         return render_pdf_view(request, "etiqueta", 
                           'tags/tag_ packing.html', context)
make_tag_packing_pdf.short_description = "Download packing label"



class SustanceAdmin(admin.ModelAdmin):
    actions = [make_tag_pdf,make_tag_packing_pdf]

class TipsAdmin(admin.ModelAdmin):
    model = Tip
    filter_horizontal = ('combinations',)         


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    filter_horizontal = ('warning_class','tips','prudence','pictogram')   


admin.site.register(Sustance,SustanceAdmin) # sustance
admin.site.register(Component) # sustance
admin.site.register(Pictogram) # SGA Control

admin.site.register(Product) # SGA Control
admin.site.register(Tip,TipsAdmin) # SGA Control
admin.site.register(Prudence) # SGA Control
admin.site.register(Category,CategoryAdmin) # SGA Control
admin.site.register(SGAIndicator)
admin.site.register(Provider)