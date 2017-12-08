from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'MASCC', views.MASCC, name='MASCC'),
    url(r'cpoe', views.cpoe, name='cpoe'),
    url(r'labEntry', views.MASCC, name='labEntry'),
    url(r'infobutton', views.infobutton, name='index.urls'),
]