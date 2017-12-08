from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'MASCC', views.MASCC, name='MASCC'),
    url(r'cpoe', views.cpoe, name='cpoe'),
    url(r'cpoehigh', views.cpoe, name='cpoehigh'),
    url(r'labEntry', views.labEntry, name='labEntry'),
    url(r'proceed', views.labEntry, name='proceed'),
    url(r'infobutton', views.infobutton, name='index.urls'),
]