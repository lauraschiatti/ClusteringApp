from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import os

from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':# if this is a POST request we need to process the form data
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else: # if a GET (or any other method) we'll create a blank form
        form = UploadFileForm()
    return render(request, 'rankorder/index.html', {'form': form})

#save file data on local file
def handle_uploaded_file(f):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #path rankorder folder
    filepath = os.path.join(BASE_DIR, 'files/weakconcepts.txt')
    with open(filepath, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
