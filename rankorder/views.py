from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

import os

from .forms import UploadFileForm

from .rankorder import *

#@csrf_protect
def upload_file(request):
    request.session['file'] = False #use session
    if request.method == 'POST':# if this is a POST request we need to process the form data
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            #name = file.name
            content_type = file.content_type
            #size = file.size

            if content_type != 'text/plain':
                form = UploadFileForm()
            else:
                handle_uploaded_file(file)
                request.session['file'] = True #use session
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
    if request.session.get('file') == True: #verify session var to show preview or not
        return render(request, 'rankorder/preview.html')
    else:
        return HttpResponseRedirect('/rankorder/file')

def algorythm(request):
    if request.session.get('file') == True: #verify session var to show preview or not

        #Rank Order Algorithm: Step by Step
        matrix = get_data_from_file() #data file

        binaryArray, binaryArrayString, linesWeightArray, linesPows = reorder_matrix_lines(matrix)

        linesWeightArray.insert(0, "Wi") #insert at the beginning
        linesPows.insert(0, "") #insert at the beginning

        data = zip(matrix, linesWeightArray, linesPows) #iterate multiple lists

        return render(request, 'rankorder/algorythm.html', {'data': data, 'binaryArrayString': binaryArrayString, 'orderedMatrix': orderedMatrix})
    else:
        return HttpResponseRedirect('/rankorder/file')

def graphs(request):
    if request.session.get('file') == True: #verify session var to show preview or not
        return render(request, 'rankorder/graphs.html')
    else:
        return HttpResponseRedirect('/rankorder/file')

def final(request):
    del request.session["file"]  # Clear item from the session:
    return render(request, 'rankorder/final.html')
