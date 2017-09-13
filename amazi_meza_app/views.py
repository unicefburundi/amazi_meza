from django.shortcuts import render
import json
from amazi_meza_app.models import *
from django.core import serializers
from django.http import HttpResponse
import datetime
import pandas as pd
import unicodedata
from django.db.models import Count, Value

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

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
    d["pagetitle"] = "Mapping"
    d["provinces"] = Province.objects.all()
    return render(request, 'mapping.html', d)

def finance(request):
    d = {}
    return render(request, 'finance.html', d)

def getCommunesInProvince(request):
    response_data = {}
    if request.method == 'POST':
        json_data = json.loads(request.body)
        code = json_data['code']
        if (code):
            communes = Commune.objects.filter(province=Province.objects.get(code=code))
            response_data = serializers.serialize('json', communes)
        return HttpResponse(response_data, content_type="application/json")


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

            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            if (colline_list):
                wp_pb_reports = WaterPointProblem.objects.filter(water_point__colline__in = colline_list, report_date__range = (start_date, end_date + datetime.timedelta(days=1)))

            wp_pb_reports_1 = serializers.serialize('python', wp_pb_reports)
            columns = [r['fields'] for r in wp_pb_reports_1]
            response_data = json.dumps(columns, default=date_handler)
            rows = json.loads(response_data)

            for r in rows:
                concerned_w_s_endpoint = WaterSourceEndPoint.objects.get(id = r["water_point"])
                r["colline_name"] = concerned_w_s_endpoint.colline.name
                r["commune_name"] = concerned_w_s_endpoint.colline.commune.name

                concerned_w_p_pbm_type = WaterPointProblemTypes.objects.get(id = r["problem"])
                r["w_p_pbm_type_name"] = concerned_w_p_pbm_type.problem_type_name

                r["report_date"] = unicodedata.normalize('NFKD', r["report_date"]).encode('ascii','ignore')[0:10]


            wp_pb_reports = WaterPointProblem.objects.filter(water_point__colline__in = colline_list, report_date__range = (start_date, end_date + datetime.timedelta(days=1))).values("problem__problem_type_name").annotate(number=Count('problem__problem_type_name'))
            

            frequent_problems_categ = []

            for r in wp_pb_reports:
                obj = {}
                obj[unicodedata.normalize('NFKD', r["problem__problem_type_name"]).encode('ascii','ignore')] = r["number"]
                frequent_problems_categ.append(obj)

            data_pieChart = []
            pieChart_freq_pbm_cat = []

            for wpp in frequent_problems_categ:
                one_item = {}
                k, v = wpp.items()[0]
                one_item["name"] = k
                one_item["y"] = v
                pieChart_freq_pbm_cat.append(one_item)

        rows = json.dumps(rows, default=date_handler)
        pieChart_freq_pbm_cat = json.dumps(pieChart_freq_pbm_cat, default=date_handler)

        all_data = json.dumps({'rows': rows, 'data': pieChart_freq_pbm_cat,})

        return HttpResponse(all_data, content_type="application/json")




def get_number_of_water_points(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        level = json_data['level']
        code = json_data['code']
        location_number_of_wp = ""
        all_data = []
        barChart_location_number_of_wp = []
        if (level):
            colline_list = None
            if (level == "colline"):
                colline_list = Colline.objects.filter(code = code)
                location_number_of_wp = WaterSourceEndPoint.objects.filter(colline__in = colline_list).values("colline__name").annotate(number=Count('colline__name'))
            
                for wpl in location_number_of_wp:
                    one_item = {}
                    one_item["name"] = wpl["colline__name"]
                    one_item["y"] = wpl["number"]
                    one_item["name: 'Mi"] = wpl["colline__name"]
                    barChart_location_number_of_wp.append(one_item)
            elif (level == "commune"):
                commune_list = Commune.objects.filter(code = code)
                if (commune_list):
                    colline_list = Colline.objects.filter(commune__in = commune_list)
                    location_number_of_wp = WaterSourceEndPoint.objects.filter(colline__in = colline_list).values("colline__commune__name").annotate(number=Count('colline__commune__name'))
            
                    for wpl in location_number_of_wp:
                        one_item = {}
                        one_item["name"] = wpl["colline__commune__name"]
                        one_item["y"] = wpl["number"]
                        one_item["name: 'Mi"] = wpl["colline__commune__name"]
                        barChart_location_number_of_wp.append(one_item)
            elif (level == "province"):
                province_list = Province.objects.filter(code = code)
                if (province_list):
                    commune_list = Commune.objects.filter(province__in = province_list)
                    if (commune_list):
                        colline_list = Colline.objects.filter(commune__in = commune_list)
                        location_number_of_wp = WaterSourceEndPoint.objects.filter(colline__in = colline_list).values("colline__commune__name").annotate(number=Count('colline__commune__name'))
                
                        for wpl in location_number_of_wp:
                            one_item = {}
                            one_item["name"] = wpl["colline__commune__name"]
                            one_item["y"] = wpl["number"]
                            one_item["name: 'Mi"] = wpl["colline__commune__name"]
                            barChart_location_number_of_wp.append(one_item)
            elif (level == "national"):
                colline_list = Colline.objects.all()
                location_number_of_wp = WaterSourceEndPoint.objects.filter(colline__in = colline_list).values("colline__commune__province__name").annotate(number=Count('colline__commune__province__name'))

                for wpl in location_number_of_wp:
                    one_item = {}
                    one_item["name"] = wpl["colline__commune__province__name"]
                    one_item["y"] = wpl["number"]
                    one_item["name: 'Mi"] = wpl["colline__commune__province__name"]
                    barChart_location_number_of_wp.append(one_item)

        
        data = json.dumps(barChart_location_number_of_wp, default=date_handler)

        return HttpResponse(data, content_type="application/json")