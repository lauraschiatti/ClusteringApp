from django.shortcuts import render


def get_index(request):
    return render(request, 'home.html', {})

def get_team(request):
    return render(request, 'team.html', {})

def get_about(request):
    return render(request, 'about.html', {})