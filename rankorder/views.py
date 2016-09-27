from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import shutil


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
                return HttpResponseRedirect('/rankorder/preview')

    else: # if a GET (or any other method) we'll create a blank form
        form = UploadFileForm()
    return render(request, 'rankorder/index.html', {'form': form})

#save file data on local file
def handle_uploaded_file(f):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(BASE_DIR, 'files/rankorder/weakconcepts.txt')

    with open(filepath, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)


def preview(request):
    #send file data for preview

    return render(request, 'rankorder/preview.html')

def algorythm(request):
    #Process data

    return render(request, 'rankorder/algorythm.html')
