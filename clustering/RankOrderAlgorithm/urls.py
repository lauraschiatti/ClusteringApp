from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rankorder/$', views.hola_mundo, name='rank'),
]
