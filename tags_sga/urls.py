from django.conf.urls import url, include
from django.urls import path


from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


from .views import   Sustance_detail,Sustance_pdf
from .views import ListSustanceView, CreateSustanceView, UpdateSustanceView

urlpatterns = [
     path('sustance/',ListSustanceView.as_view(), name="sustance-list"),
     path('sustance/detail/<str:sustance_pk>/', Sustance_detail, name="sustance-detail"),
     path('sustance/generate/<str:sustance_pk>/', Sustance_pdf, name="sustance-generate"),
     path('sustance/create', CreateSustanceView.as_view(), name='sustance_create'),
     path('sustance/update/<str:sustance_pk>/', UpdateSustanceView.as_view(), name='sustance_update'),
]

# login actions
urlpatterns +=[
    url(r'^accounts/login/$', auth_views.login,
        {'template_name': 'login.html'}, name='login'),
    
    url(r'^accounts/logout/$', auth_views.logout, {
        'next_page': reverse_lazy('sustance-list')},
        name='logout'),
   ]
# urlpatterns = [
#     path('sustance/', Sustance_list, name="sustance-list"),
#     path('sustance/<str:sustance_pk>/', Sustance_detail, name="sustance-detail"),
#     path('sustance/<str:sustance_pk>/generate_tag/', Sustance_pdf, name="sustance-generate"),
# ]