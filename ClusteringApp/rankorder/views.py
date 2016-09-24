from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import os

from .forms import UploadFileForm

#@csrf_protect
def upload_file(request):
    if request.method == 'POST':# if this is a POST request we need to process the form data
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            name = file.name
            content_type = file.content_type
            size = file.size

            if content_type != 'text/plain':
                form = UploadFileForm()
            else:
                handle_uploaded_file(file)
                return HttpResponseRedirect('/')

    else: # if a GET (or any other method) we'll create a blank form
        form = UploadFileForm()
    return render(request, 'rankorder/index.html', {'form': form})

#save file data on local file
def handle_uploaded_file(f):
    print "f", f
    """BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #path rankorder folder
    filepath = os.path.join(BASE_DIR, 'files/weakconcepts.txt')
    with open(filepath, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)"""
