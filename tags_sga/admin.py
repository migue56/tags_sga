from django.contrib import admin
from .models import (
    Pictogram,
    Tip,
    Prudence,
    Category,
    SGAIndicator,
    Component,
    Sustance,
    )
admin.site.register([Sustance, Component]) # sustance


admin.site.register([Pictogram,Tip,Prudence,Category,SGAIndicator]) # SGA Control
