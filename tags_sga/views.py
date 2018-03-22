from django.shortcuts import render

from .models import (
    Pictogram,
    Tip,
    Prudence,
    Category,
    SGAIndicator,
    Component,
    Sustance,
    )


from cruds_adminlte.crud import CRUDView

class SustanceCRUD(CRUDView):
    model = Sustance
    #template_name_base='ccruds'  #customer cruds => ccruds
    namespace = None
    check_login = False
    check_perms = False
    views_available=['create', 'list', 'delete', 'update', 'detail']
    #fields = ['name','email']
    related_fields = ['componets']
