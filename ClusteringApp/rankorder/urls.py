from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rankorder/$', views.get_index, name='rank'),
]
