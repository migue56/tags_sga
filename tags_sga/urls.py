from django.conf.urls import url, include
from django.urls import path
from .views import  Sustance_list, Sustance_detail,Sustance_pdf

urlpatterns = [
    path('sustance/', Sustance_list, name="sustance-list"),
    path('sustance/<str:sustance_pk>/', Sustance_detail, name="sustance-detail"),
    path('sustance/<str:sustance_pk>/generate_tag/', Sustance_pdf, name="sustance-generate"),
]