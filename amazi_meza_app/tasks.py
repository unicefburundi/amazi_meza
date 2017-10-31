#  -*- coding: utf-8 -*-
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import pytz
from django.conf import settings
import requests
import json
from amazi_meza_app.models import *
# import datetime
from datetime import datetime, timedelta, time

logger = get_task_logger(__name__)


def send_sms_through_rapidpro(args):
    ''' 
    This function sends messages through rapidpro. Contact(s) and the
    message to send to them must be in args['data']
    '''
    print("--Begin send_sms_through_rapidpro-- Amazi Meza")
    token = getattr(settings, 'TOKEN', '')
    data = args['data']
    print(data)
    response = requests.post(settings.RAPIDPRO_BROADCAST_URL, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data=json.dumps(data))
    print("response :")
    print(response)
    print("--Finish send_sms_through_rapidpro-- Amazi Meza")



#@periodic_task(run_every=(crontab(minute=30, hour='11')), name="tasks.inform_on_inactive_water_points", ignore_result=True)
def inform_on_inactive_water_points():
    '''
    This task sends sms to a local reporter and his/her supervisor if there is a long time
    without sms about repair of a reported water point problem
    '''
    print("-Begin inform_on_inactive_water_points")

    settings_to_use = Setting.objects.filter(setting_code = "RAUWPP")
    if len(settings_to_use) > 0:
        settings_to_use = settings_to_use[0]
    else:
        time_ob = TimeMeasuringUnit.objects.get_or_create(code="H", description="Hour")
        settings_to_use = Setting.objects.create(setting_code = "RAUWPP", setting_name = "Condition for sending Reminders About Unresolved WP Problems", setting_value = 72, time_measuring_unit = time_ob)


    value_for_time = settings_to_use.setting_value

    # Let's convert value_for_time to a number
    try:
        value_for_time = int(value_for_time)
    except:
        info = "Exception. The setting value in Settings model is not a number"
        return

    time_unit = settings_to_use.time_measuring_unit.code

    limit_time = ""

    if(time_unit.startswith("m") or time_unit.startswith("M")):
        # The time measuring unit used is minutes
        # limit_time = datetime.datetime.now() - datetime.timedelta(minutes = value_for_time)
        limit_time = datetime.now() - timedelta(minutes = value_for_time)
    if(time_unit.startswith("h") or time_unit.startswith("H")):
        # The time measuring unit used is hours
        # limit_time = datetime.datetime.now() - datetime.timedelta(hours = value_for_time)
        limit_time = datetime.now() - timedelta(hours = value_for_time)

    # if not isinstance(limit_time, datetime.datetime):
    if not isinstance(limit_time, datetime):
        info = "Something went wrong for limit time"
        return

    concerned_wp_problems = WaterPointProblem.objects.filter(problem_solved = False, report_date__date = limit_time)
    #concerned_wp_problems = WaterPointProblem.objects.filter(problem_solved = False, report_date__date__lte = limit_time)
    
    #send messages to the corresponding local level and his supervisor
    print("-------------------")
    print(concerned_wp_problems)

    if(len(concerned_wp_problems) > 0):
        for wpp in concerned_wp_problems:
            water_point_name = wpp.water_point.water_point_name
            wpp_code = wpp.wpp_code
            print(water_point_name)
            print(wpp_code)
