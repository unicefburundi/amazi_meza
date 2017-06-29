from django.shortcuts import render

def landing(request):
    d = {}
    return render(request, 'landing_page.html', d)


def home(request):
    d = {}
    return render(request, 'home.html', d)


def problems(request):
    d = {}
    return render(request, 'problems.html', d)


def mapping(request):
    d = {}
    return render(request, 'mapping.html', d)

def finance(request):
    d = {}
    return render(request, 'finance.html', d)
