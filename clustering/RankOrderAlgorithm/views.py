from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def hola_mundo(request):
    template = loader.get_template('rankorder/index.html')
    return HttpResponse(template.render(request))
