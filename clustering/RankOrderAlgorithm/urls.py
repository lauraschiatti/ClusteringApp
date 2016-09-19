from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^hola/$', views.hola_mundo, name='hola'),
]
