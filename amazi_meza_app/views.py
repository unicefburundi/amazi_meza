from django.shortcuts import render
import json
from amazi_meza_app.models import *
from django.core import serializers
from django.http import HttpResponse
import datetime
import pandas as pd
import unicodedata
from django.db.models import Count, Value, Sum
from django.conf import settings
from operator import itemgetter

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
    d["all_water_points"] = WaterSourceEndPoint.objects.all()
    print("111>>>")
    print(d["all_water_points"])
    print("111---")
    return render(request, 'mapping.html', d)

def finance(request):
    d = {}
    d["pagetitle"] = "Finance"
    d["provinces"] = Province.objects.all()
    d["all_communes"] = Commune.objects.all()
    d["expenditures"] = ExpenditureCategory.objects.all()
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
    # View for "Problems" page
    response_data = {}
    if request.method == 'POST':
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
                colline_list = Colline.objects.filter(code=code)

            elif (level == "commune"):
                commune_list = Commune.objects.filter(code=code)
                if (commune_list):
                    colline_list = Colline.objects.filter(commune__in=commune_list)
            elif (level == "national"):
                colline_list = Colline.objects.all()

            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

            if (colline_list):
                wp_pb_reports = WaterPointProblem.objects.filter(water_point__colline__in=colline_list, report_date__range=(start_date, end_date + datetime.timedelta(days=1)))

            wp_pb_reports_1 = serializers.serialize('python', wp_pb_reports)
            columns = [r['fields'] for r in wp_pb_reports_1]
            response_data = json.dumps(columns, default=date_handler)
            rows = json.loads(response_data)


            wpp_resolvers = {}
            resolvers_set = WaterPointProblemResolver.objects.all()
            if len(resolvers_set) > 0:
                for r in resolvers_set:
                    #wpp_resolvers[r.resolver_level_code] = r.resolver_level_name
                    wpp_resolvers[r.id] = unicodedata.normalize('NFKD', r.resolver_level_name).encode('ascii', 'ignore')


            for r in rows:
                concerned_w_s_endpoint = WaterSourceEndPoint.objects.get(id=r["water_point"])
                r["colline_name"] = concerned_w_s_endpoint.colline.name
                r["commune_name"] = concerned_w_s_endpoint.colline.commune.name

                concerned_w_p_pbm_type = WaterPointProblemTypes.objects.get(id=r["problem"])
                r["w_p_pbm_type_name"] = concerned_w_p_pbm_type.problem_type_name

                r["report_date"] = unicodedata.normalize('NFKD', r["report_date"]).encode('ascii','ignore')[0:10]

                if r["case_of_diarrhea"]:
                    r["case_of_diarrhea"] = "Yes"
                else:
                    r["case_of_diarrhea"] = "No"

                if r["problem_solved"]:
                    r["problem_solved"] = "Resolved"
                else:
                    r["problem_solved"] = "Not yet resolved"
                    r["resolve_date"] = ""

                if r["resolved_at"]:
                    resolver_level = r["resolved_at"]
                    r["resolver_level"] = wpp_resolvers[resolver_level]
                else:
                    r["resolver_level"] = " "

                #r["report_date"] = unicodedata.normalize('NFKD', r["report_date"]).encode('ascii', 'ignore')[0:10]

            # wp_pb_reports = WaterPointProblem.objects.filter(water_point__colline__in = colline_list, report_date__range = (start_date, end_date + datetime.timedelta(days=1))).values("problem__problem_type_name").annotate(number=Count('problem__problem_type_name'))
            wp_pb_reports = WaterPointProblem.objects.filter(water_point__colline__in=colline_list, report_date__range=(start_date, end_date + datetime.timedelta(days=1))).values("problem__problem_type_description").annotate(number=Count('problem__problem_type_description'))


            frequent_problems_categ = []

            for r in wp_pb_reports:
                obj = {}
                obj[unicodedata.normalize('NFKD', r["problem__problem_type_description"]).encode('ascii', 'ignore')] = r["number"]
                frequent_problems_categ.append(obj)

            pieChart_freq_pbm_cat = []

            for wpp in frequent_problems_categ:
                one_item = {}
                k, v = wpp.items()[0]
                one_item["name"] = k
                one_item["y"] = v
                pieChart_freq_pbm_cat.append(one_item)

        rows = json.dumps(rows, default=date_handler)
        pieChart_freq_pbm_cat = json.dumps(pieChart_freq_pbm_cat, default=date_handler)


        number_wp_pb_per_loc = WaterPointProblem.objects.filter(water_point__colline__in = colline_list, report_date__range = (start_date, end_date + datetime.timedelta(days=1))).values("water_point__colline__name").annotate(number=Count('water_point__colline__name'))

        bar_chart_location_number_wpp = []
        for lo in number_wp_pb_per_loc:
            one_item = {}
            one_item["name"] = lo["water_point__colline__name"]
            one_item["y"] = lo["number"]
            one_item["name: 'Mi"] = lo["water_point__colline__name"]
            bar_chart_location_number_wpp.append(one_item)


        # all_data = json.dumps({'rows': rows, 'data': pieChart_freq_pbm_cat,})
        all_data = json.dumps({'rows': rows, 'data': pieChart_freq_pbm_cat,  'location_number_wpp': bar_chart_location_number_wpp,})
        return HttpResponse(all_data, content_type="application/json")


def get_expenditures_info(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        level = json_data['level']
        code = json_data['code']
        start_date = json_data['start_date']
        end_date = json_data['end_date']
        exp_reports = ""
        all_data = []

        if (level):
            commune_list = None
            if (level == "commune"):
                commune_list = Commune.objects.filter(code = code)
            if(level == "province"):
                province = Province.objects.filter(code = code)
                if(province):
                    commune_list = Commune.objects.filter(province__in = province)
            if(level == "national"):
                commune_list = Commune.objects.all()

            #Below row will be changed and use reporting_year and reporting_month instead of
            #reception_date
            
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            end_date = end_date + datetime.timedelta(days=1)
            
            exp_reports = MonthlyExpenditure.objects.filter(commune__in = commune_list, reception_date__range = (start_date, end_date))

            exp_reports_1 = serializers.serialize('python', exp_reports)
            columns = [r['fields'] for r in exp_reports_1]
            exp_reports = json.dumps(columns, default=date_handler)
            exp_reports = json.loads(exp_reports)

            for exp in exp_reports:
                concerned_commune = Commune.objects.filter(id = exp["commune"])
                if len(concerned_commune) > 0:
                    concerned_commune = concerned_commune[0]
                    exp["commune_name"] = concerned_commune.name
                concerned_exp_cat = ExpenditureCategory.objects.filter(id = exp["expenditure"])
                if len(concerned_exp_cat) > 0:
                    concerned_exp_cat = concerned_exp_cat[0]
                    exp["expenditure_cat_name"] = concerned_exp_cat.expenditure_category_name

            exp_reports = json.dumps(exp_reports, default=date_handler)




            number_of_exp_per_categories = MonthlyExpenditure.objects.filter(commune__in = commune_list, reception_date__range = (start_date, end_date)).values("expenditure__expenditure_category_name").annotate(number=Sum('expenditure_amount'))
            #pieChart_exp_per_cat = json.dumps(number_of_exp_per_categories, default=date_handler)

            #all_data = json.dumps({'rows': exp_reports, 'data': pieChart_exp_per_cat,})

            pieChart_exp_cat = []

            for exp in number_of_exp_per_categories:
                one_item = {}
                #k, v = wpp.items()[0]
                one_item["name"] = exp["expenditure__expenditure_category_name"].encode('ascii','ignore')
                one_item["y"] = exp["number"]
                pieChart_exp_cat.append(one_item)

            pieChart_exp_cat = json.dumps(pieChart_exp_cat, default=date_handler)



            #Compute expenditure per location
            exp_per_location = MonthlyExpenditure.objects.filter(commune__in = commune_list, reception_date__range = (start_date, end_date)).values("commune__name").annotate(number=Sum('expenditure_amount'))
            barChart_location_expenditure = []
            for exp_loc in exp_per_location:
                one_item = {}
                one_item["name"] = exp_loc["commune__name"]
                one_item["y"] = exp_loc["number"]
                one_item["name: 'Mi"] = exp_loc["commune__name"]
                barChart_location_expenditure.append(one_item)


            #Compute icome per location
            income_per_location = MonthlyIncome.objects.filter(commune__in = commune_list, reception_date__range = (start_date, end_date)).values("commune__name").annotate(number=Sum('total_income'))
            barChart_location_income = []
            for in_loc in income_per_location:
                one_item = {}
                one_item["name"] = in_loc["commune__name"]
                one_item["y"] = in_loc["number"]
                one_item["name: 'Mi"] = in_loc["commune__name"]
                barChart_location_income.append(one_item)


            all_data = json.dumps({'rows': exp_reports, 'data': pieChart_exp_cat, 'location_expendi': barChart_location_expenditure, 'location_income': barChart_location_income,})


            


    return HttpResponse(all_data, content_type="application/json")



def exp_vs_in(request):
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)

        level = json_data['level']
        code = json_data['code']
        year = int(json_data['year'])


        if (level):
            commune_list = None
            if (level == "commune"):
                commune_list = Commune.objects.filter(code = code)
                incomes = MonthlyIncome.objects.filter(commune__in = commune_list, reporting_year = year).values("reporting_month").annotate(number=Sum('total_income'))
                expenditure = MonthlyExpenditure.objects.filter(commune__in = commune_list, reporting_year = year).values("reporting_month").annotate(number=Sum('expenditure_amount'))
            if(level == "national"):
                commune_list = Commune.objects.all()[0]
                incomes = MonthlyIncome.objects.filter(commune__in = commune_list, reporting_year = year).values("reporting_month").annotate(number=Sum('total_income'))
                expenditure = MonthlyExpenditure.objects.filter(commune__in = commune_list, reporting_year = year).values("reporting_month").annotate(number=Sum('expenditure_amount'))

            months_mames = getattr(settings, 'MONTHS_NAMES', '')

            inc = []
            for i in incomes:
                one_item = {}
                one_item["month_number"] = i["reporting_month"]
                one_item["y"] = i["number"]
                one_item["month_name"] = months_mames[str(i["reporting_month"])]
                inc.append(one_item)

            exp = []
            for i in expenditure:
                one_item = {}
                one_item["month_number"] = i["reporting_month"]
                one_item["y"] = i["number"]
                one_item["month_name"] = months_mames[str(i["reporting_month"])]
                exp.append(one_item)

            inc = sorted(inc, key=itemgetter('month_number'))
            exp = sorted(exp, key=itemgetter('month_number'))

            current_month = datetime.datetime.now().month

            incomes_values_list = []
            if len(inc):
                all_income = inc[0]["y"]
                for i in range(1,current_month+1):
                    ob = 0
                    found = False
                    found_value = 0
                    while not found and ob < len(inc):
                        if(inc[ob]["month_number"]) == i:
                            found = True
                            found_value = inc[ob]["y"]
                        else:
                            ob = ob + 1
                    all_income = all_income + found_value
                    incomes_values_list.append(all_income)
            incomes = {}
            incomes["name"] = "Cumulative Income"
            incomes["data"] = incomes_values_list

            expenditure_values_list = []
            if len(exp):
                all_expenditure = exp[0]["y"]
                for i in range(1,current_month+1):
                    ob = 0
                    found = False
                    found_value = 0
                    while not found and ob < len(exp):
                        if(exp[ob]["month_number"]) == i:
                            found = True
                            found_value = exp[ob]["y"]
                        else:
                            ob = ob + 1
                    all_expenditure = all_expenditure + found_value
                    expenditure_values_list.append(all_expenditure)
            expenditures = {}
            expenditures["name"] = "Cumulative Expenditure"
            expenditures["data"] = expenditure_values_list


    all_data = json.dumps({'incomes': incomes, 'expenditures': expenditures,})
    #all_data = json.dumps({'incomes': inc, 'expenditure': exp,})

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
                    #location_number_of_wp = WaterSourceEndPoint.objects.filter(colline__in = colline_list).values("colline__commune__name").annotate(number=Count('colline__commune__name'))
                    location_number_of_wp = WaterSourceEndPoint.objects.filter(colline__in = colline_list).values("colline__name").annotate(number=Count('colline__name'))


                    for wpl in location_number_of_wp:
                        one_item = {}
                        #one_item["name"] = wpl["colline__commune__name"]
                        one_item["name"] = wpl["colline__name"]
                        one_item["y"] = wpl["number"]
                        #one_item["name: 'Mi"] = wpl["colline__commune__name"]
                        one_item["name: 'Mi"] = wpl["colline__name"]
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