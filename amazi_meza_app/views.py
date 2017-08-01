from django.shortcuts import render
import json
from amazi_meza_app.models import *
from django.core import serializers
from django.http import HttpResponse

def landing(request):
    d = {}
    return render(request, 'landing_page.html', d)


def home(request):
    d = {}
    return render(request, 'home.html', d)


def problems(request):
    d = {}
    d["pagetitle"] = "Problems"
    d["communes"] = Commune.objects.all()
    return render(request, 'problems.html', d)

def mapping(request):
    d = {}
    return render(request, 'mapping.html', d)

def finance(request):
    d = {}
    return render(request, 'finance.html', d)

def getCollinesInCommune(request):
    response_data = {}
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        code = json_data['code']
        if (code):
            collines = Colline.objects.filter(commune=Commune.objects.get(code=code))
            response_data = serializers.serialize('json', collines)
        return HttpResponse(response_data, content_type="application/json")



def getwanteddata(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        level = json_data['level']
        code = json_data['code']
        start_date = json_data['start_date']
        end_date = json_data['end_date']
        wp_pb_reports = ""
        all_data = []

        if (level):
            colline_list = None
            if (level == "colline"):
                colline_list = Colline.objects.filter(code = code)

            elif (level == "commune"):
                commune_list = Commune.objects.filter(code = code)
                if (commune_list):
                    colline_list = Colline.objects.filter(commune__in = commune_list)
            elif (level == "national"):
                colline_list = Colline.objects.all()

            if (colline_list):
                wp_pb_reports = WaterPointProblem.objects.all()

        response_data = serializers.serialize('json', wp_pb_reports)
        return HttpResponse(response_data, content_type="application/json")