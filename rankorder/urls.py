from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^rankorder/file/$', views.upload_file, name='upload_file'),
    url(r'^rankorder/preview/$', views.preview, name='preview'),
]