from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rankorder/file/$', views.upload_file, name='upload_file'),
    url(r'^rankorder/preview/$', views.preview, name='preview'),
    url(r'^rankorder/algorythm/$', views.algorythm, name='algorythm'),
    url(r'^rankorder/graphs/$', views.graphs, name='graphs'),
    url(r'^rankorder/final/$', views.final, name='final')
]
