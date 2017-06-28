from django.shortcuts import render

def home(request):
    d = {}
    return render(request, 'landing_page.html', d)
