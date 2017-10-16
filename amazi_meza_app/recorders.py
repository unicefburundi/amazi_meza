from public_administration_structure_app.models import *
from amazi_meza_app.models import *

import datetime
from django.conf import settings
import re

def check_colline(args):
    ''' This function checks if the colline name sent by the reporter exists '''
    the_colline_name = args['text'].split('#')[1]
    concerned_facility = CDS.objects.filter(code = the_facility_code)
    if (len(concerned_facility) > 0):
        args['valide'] = True
        args['info_to_contact'] = "Le code CDS envoye est reconnu."
    else:
        args['valide'] = False
        # args['info_to_contact'] = "Erreur. Le code envoye n est pas associe a un CDS. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
        args['info_to_contact'] = "Ikosa. Wanditse inomero y ivuriro itabaho. Mu gukosora, subira urungike iyo mesaje itangurwa na '"+args['mot_cle']+"' yanditse neza"


def check_number_of_values(args):
    ''' This function checks if the message sent is composed by an expected number of values '''
    expected_number_of_values_string = args["expected_number_of_values"]
    expected_number_of_values_int = int(expected_number_of_values_string)


    if len(args['text'].split('#')) < expected_number_of_values_int:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
    if len(args['text'].split('#')) > expected_number_of_values_int:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Pour corriger, veuillez reenvoyer un message corrige et commencant par le mot cle "+args['mot_cle']
    if len(args['text'].split('#')) == expected_number_of_values_int:
        args['valide'] = True
        args['info_to_contact'] = "Le nombre de valeurs envoye est correct."


def check_has_already_session(args):
    '''This function checks if this contact has a session'''
    same_existing_local_temp = LocalLevelReporter.objects.filter(reporter_phone_number = args['phone'])
    if len(same_existing_local_temp ) > 0:
        same_existing_local_temp = same_existing_local_temp[0]
        same_existing_local_temp.delete()
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous devriez envoyer le numero de telephone de votre superviseur seulement. Pour corriger, veuillez recommencer l enregistrement."
        return

    same_existing_commune_level_temp = CommuneLevelReporters.objects.filter(reporter_phone_number = args['phone'])
    if len(same_existing_commune_level_temp) > 0:
        same_existing_commune_level_temp = same_existing_commune_level_temp[0]
        same_existing_commune_level_temp.delete()
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous devriez envoyer le numero de telephone de votre superviseur seulement. Pour corriger, veuillez recommencer l enregistrement."
        return

    
    args['valide'] = True
    args['info_to_contact'] = "Ok."


def check_if_is_commune_level_reporter(args):
    ''' This function checks if the contact who sent the current message is a commune level reporter '''
    args['valide'] = False
    concerned_reporter = CommuneLevelReporters.objects.filter(reporter_phone_number = args['phone'])
    if len(concerned_reporter) > 0:
        args['valide'] = True
        args['reporter_category'] = "C"
        args['the_sender'] = concerned_reporter[0]

    #The below code will be in the function which checks if someone is amoung recorded
    #local level reporters
    '''concerned_reporter = LocalLevelReporter.objects.filter(reporter_phone_number = args['phone'])
    if len(concerned_chw) > 0:
        args['valide'] = True
        args['reporter_category'] == "L"
        one_concerned_reporter = concerned_reporter[0]'''


    if len(concerned_reporter) < 1:
        # This person is not in the list of reporters
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports. Veuillez vous enregistrer en envoyant le message d enregistrement"
        return

    #args['the_sender'] = concerned_reporter
    args['the_commune'] = args['the_sender'].commune
    args['info_to_contact'] = "Vous etes reconnu comme rapporteur"


def check_if_is_colline_level_reporter(args):
    ''' This function checks if the contact who sent the current message is a colline level reporter '''
    args['valide'] = False
    concerned_reporter = LocalLevelReporter.objects.filter(reporter_phone_number = args['phone'])
    if len(concerned_reporter) > 0:
        args['valide'] = True
        args['reporter_category'] = "L"
        args['the_sender'] = concerned_reporter[0]

    if len(concerned_reporter) < 1:
        # This person is not in the list of reporters
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports. Veuillez vous enregistrer en envoyant le message d enregistrement"
        return

    args['the_colline'] = args['the_sender'].colline
    args['the_commune'] = args['the_colline'].commune
    args['info_to_contact'] = "Vous etes reconnu comme rapporteur"

def identify_water_point(args):
    ''' This function identify a water point a given reporter reports for '''

    water_point_set = WaterSourceEndPoint.objects.filter(reporter = args['the_sender'])

    if len(water_point_set) > 0:
        args['valide'] = True
        args['concerned_water_point'] = water_point_set[0]
        args['info_to_contact'] = "Le point d eau concerne est reconnu"
    else:
        args['valide'] = False
        args['info_to_contact'] = "Le point d eau pour lequel vous rapportez n est pas reconnu"

def check_commune_exists(args):
    ''' This function checks if the commune exists '''
    commune_code = args["commune_code"]
    try:
        commune_code = int(commune_code)
    except:
        args['valide'] = False
        args['info_to_contact'] = "Le code ne peut etre compose que par des chiffres."
    else:
        commune_set = Commune.objects.filter(code = commune_code)
        if len(commune_set) > 0:
            args["concerned_commune"] = commune_set[0]
            args["valide"] = True
        else:
            args["info_to_contact"] = "Erreur. Il n y a pas de commune ayant ce code"
            args["valide"] = False

def check_commune_colline_names_valide(args):
    ''' This function checks if the commune and the colline names are valid '''
    commune_name = args["commune_name"].upper()
    colline_name = args["colline_name"].upper()

    colline_set = Colline.objects.filter(name__iexact= colline_name, commune__name__iexact= commune_name)
    if len(colline_set) > 0:
        args["concerned_colline"] = colline_set[0]
        args["valide"] = True
        args["info_to_contact"] = "Il y a la colline '"+colline_name+"' enregistree dans la commune '"+commune_name+"'."
    else:
        args["info_to_contact"] = "Erreur. Il n y a pas de colline '"+colline_name+"' enregistree dans la commune '"+commune_name+"'."
        args["valide"] = False


def check_network_registered(args):
    ''' This function checks if a water network is not already registered in a given commune '''
    args["water_network_name"] = args['text'].split('#')[1].strip().upper()
    network_set = WaterNetWork.objects.filter(commune = args['the_commune'], water_network_name = args["water_network_name"])
    if len(network_set) > 0:
        args["valide"] = True
        args["registered_water_nw"] = network_set[0]
        args["info_to_contact"] = "Ce reseau d eau est deja enregistre"
    else:
        args['valide'] = False
        args["info_to_contact"] = "Ce reseau d eau n est pas enregistre"

def check_water_network_code_valid(args):
    ''' This function checks if the water network code sent exits in a given colline '''
    water_network_code = args["water_network_code"]

    water_network_set = WaterNetWork.objects.filter(commune = args["concerned_colline"].commune, water_network_code = args["water_network_code"])

    if len(water_network_set) > 0:
        args["valide"] = True
        args["concerned_water_network"] = water_network_set[0]
        args["info_to_contact"] = "Le reseau d eau indique est bien indentifie"
    else:
        args['valide'] = False
        args["info_to_contact"] = "Erreur. Il n y a pas de reseau '"+args["water_network_code"]+"' enregistre dans la commune '"+args["concerned_colline"].commune.name+"'"


def check_water_point_name_unique_in_colline(args):
    ''' This function checks if a water point name given is not already registered '''

    water_point_name = args["water_point_name"]

    water_point_set = WaterSourceEndPoint.objects.filter(colline = args["concerned_colline"], water_point_name__iexact = water_point_name)

    if len(water_point_set) > 0:
        args["valide"] = True
        args["info_to_contact"] = "Erreur. Le point d eau '"+water_point_name.upper()+"' est deja enregistre dans la colline '"+args["concerned_colline"].name.upper()+"'"
    else:
        args["valide"] = False
        args["info_to_contact"] = "Le point d eau nomme '"+water_point_name.upper()+"' n est pas encore enregistre dans la colline '"+args["concerned_colline"].name.upper()+"'"

def check_water_point_type_exists(args):
    ''' This function checks if the water point type sent is valid '''

    water_point_type = args["water_point_type"]

    water_point_type_set = WaterPointType.objects.filter(name__iexact = water_point_type)

    if len(water_point_type_set) > 0:
        args["valide"] = True
        args["concerned_water_point_type"] = water_point_type_set[0]
        args["info_to_contact"] = "Le type du point d eau indique est reconnu"
    else:
        args["valide"] = False
        args["info_to_contact"] = "Le type du point d eau indique n est pas reconnu"

def check_w_p_problem_category_valid(args):
    ''' This function checks if the water point problem category sent is valid '''

    w_p_problem_type = args["problem_category"]

    w_p_problem_type_set = WaterPointProblemTypes.objects.filter(problem_type_name__iexact = w_p_problem_type)

    if len(w_p_problem_type_set) > 0:
        args["valide"] = True
        args["concerned_w_p_pbm_type"] = w_p_problem_type_set[0]
        args["info_to_contact"] = "Le type de probleme envoye est reconnu"
    else:
        args["valide"] = False
        args["info_to_contact"] = "Erreur. Le type de probleme envoye n est pas reconnu"

def check_water_network_problem_type(args):
    ''' This function checks if the water network problem category sent is valid '''

    network_problem_type_code = args['network_problem_type_code']

    network_problem_type_set = WaterNetworkProblemType.objects.filter(water_network_problem_code__iexact = network_problem_type_code)

    if len(network_problem_type_set) > 0:
        args["valide"] = True
        args["concerned_w_network_pbm_type"] = network_problem_type_set[0]
        args["info_to_contact"] = "Le type de probleme du reseau d eau envoye est reconnu"
    else:
        args["valide"] = False
        args["info_to_contact"] = "Erreur. Le type de probleme du reseau d eau envoye n est pas reconnu"



def check_action_taken_valid(args):
    ''' This function checks if the action taken sent is valid '''

    action_taken = args["action_taken"]

    action_taken_set = ActionsForWaterPointProblem.objects.filter(action_code__iexact = action_taken)

    if len(action_taken_set) > 0:
        args["valide"] = True
        args["concerned_action_taken"] = action_taken_set[0]
        args["info_to_contact"] = "Votre action face au probleme est reconnu"
    else:
        args["valide"] = False
        args["info_to_contact"] = "Erreur. Votre action face a ce probleme de point d eau n est pas reconnu"

def check_number_of_days_valid(args):
    ''' This function checks if the number of days sent is valid '''

    number_of_days = args["number_of_days"]

    expression = r'^[0-9]+$'

    if re.search(expression, number_of_days) is None:
        args['valide'] = False
        args["info_to_contact"] = "Erreur. Le nombre de jours envoye n est pas valide"
    else:
        args['valide'] = True
        args["info_to_contact"] = "Le nombre de jours envoye est valide"

def check_is_number(args):
    ''' This function checks if a given number is a valid number '''

    number_to_check = args['number_to_check']

    expression = r'^[0-9]+$'

    if re.search(expression, number_to_check) is None:
        args['valide'] = False
        args["info_to_contact"] = "Erreur. La valeur envoyee pour '"+args['value_meaning']+"' n est pas valide"
    else:
        args['valide'] = True
        args["info_to_contact"] = "La valeur envoyee pour '"+args['value_meaning']+"' est valide"


def check_is_year(args):
    ''' This function checks if a given number is a year '''

    number_to_check = args['number_to_check']

    expression = r'^[0-9]{4}$'

    if re.search(expression, number_to_check) is None:
        args['valide'] = False
        args["info_to_contact"] = "Erreur. La valeur envoyee pour '"+args['value_meaning']+"' n est pas valide"
    else:
        args['valide'] = True
        args["info_to_contact"] = "La valeur envoyee pour '"+args['value_meaning']+"' est valide"


def check_number_is_int(args):
    ''' This function checks if the number at the indicated position is an int '''

    indicated_position = args['number_position']
    number_to_check = args['text'].split('#')[indicated_position]

    expression = r'^[0-9]+$'

    if re.search(expression, number_to_check) is None:
        args['valide'] = False
        args["info_to_contact"] = "Erreur. La valeur en position '"+str(indicated_position)+"' n est pas valide"
    else:
        args['valide'] = True
        args["info_to_contact"] = "La valeur en position '"+str(indicated_position)+"' est valide"



def check_is_not_future_year(args):
    ''' This function cheks if the year sent is not a future year '''

    value_to_check = int(args['value_to_check'])

    current_year = datetime.datetime.now().year

    if(value_to_check > current_year):
        args['valide'] = False
        args["info_to_contact"] = "Erreur. '"+args['value_meaning']+"' ne peut pas etre une annee futur"
        return
    if(args['lower_limit']):
        if(value_to_check < args['lower_limit']):
            args['valide'] = False
            args["info_to_contact"] = "Erreur. '"+args['value_meaning']+"' ne peut pas etre inferieure a '"+str(args['lower_limit'])+"'"
            return


    args['valide'] = True
    args["info_to_contact"] = "'"+args['value_meaning']+"' est valide"


def check_month_between_1_12(args):
    ''' This function cheks if the month sent is between one and 12 '''

    value_to_check = int(args['value_to_check'])

    if((value_to_check < 1) or (value_to_check > 12)):
        args['valide'] = False
        args["info_to_contact"] = "Erreur. La valeur de '"+args['value_meaning']+"' doit etre entre 1 et 12"
    else:
        args['valide'] = True
        args["info_to_contact"] = "La valeur de '"+args['value_meaning']+"' est entre 1 et 12"


def choose_water_network_code(args):
    ''' This function choose a code to give to a water network '''
    water_network_name = args['text'].split('#')[1]
    water_network_code = len(water_network_name)

    code_valide = False

    while not code_valide:
        water_network_set = WaterNetWork.objects.filter(water_network_code = str(water_network_code))
        if len(water_network_set) < 1:
            code_valide = True
            args['water_network_code'] =  str(water_network_code)
        else:
            water_network_code = water_network_code + 1


def record_commune_level_reporter(args):
    '''This function is used to record a commune level reporter'''
    if(args['text'].split('#')[0].upper() == 'RLR'):
        args['mot_cle'] = 'RLR'
        # Because RLR is used to do the self registration and not the update, if the phone user sends a message starting with RLR and             
        # he/she is already a reporter, we don't allow him/her to continue
        check_if_is_commune_level_reporter(args)
        if(args['valide'] is True):
            # This contact is already a commune level reporter and can't do the registration the second time
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous vous etes deja enregistre. Si vous voulez modifier votre enregistrement, envoyer le message commencant par le mot cle 'RLRM'"
            return
    
        # Let's check if the message sent is composed by an expected number of values
        args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
        check_number_of_values(args)
        if not args['valide']:
            return

        # Let's check if the code of the commune is valid
        args["commune_code"] = args['text'].split('#')[2]
        check_commune_exists(args)
        if not args['valide']:
            return

        # Let's save the commune level reporter
        CommuneLevelReporters.objects.create(commune = args["concerned_commune"], reporter_phone_number = args['phone'], reporter_name = args['text'].split('#')[1], date_registered = datetime.datetime.now().date())
        args["valide"] = True
        args["info_to_contact"] = "Tu es bien enregistre dans la liste des rapporteurs du niveau communal"
    if(args['text'].split('#')[0].upper() == 'RLRM'):
        args['mot_cle'] = 'REGM'

        check_if_is_commune_level_reporter(args)
        if(args['valide'] is False):
            # This contact is not a commune level reporter and can't do the update
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Tu n es pas enregistre dans la liste des rapporteurs du niveau communal"
            return

        # Let's check if the message sent is composed by an expected number of values
        args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
        check_number_of_values(args)
        if not args['valide']:
            return

        # Let's check if the code of CDS is valid
        args["commune_code"] = args['text'].split('#')[2]
        check_commune_exists(args)
        if not args['valide']:
            return

        #Let's update this commune level reporter
        reporter_set = CommuneLevelReporters.objects.filter(reporter_phone_number = args["phone"])
        the_concerned_reporter = reporter_set[0]
        the_concerned_reporter.commune = args["concerned_commune"]
        the_concerned_reporter.reporter_name = args['text'].split('#')[1]
        the_concerned_reporter.save()
        args["valide"] = True
        args["info_to_contact"] = "Mise a jour reussie"


def record_water_network(args):
    ''' This function is used to record a water networks '''

    args['mot_cle'] = "RLC"

    check_if_is_commune_level_reporter(args)
    if(args['valide'] is False):
        # This contact is not a commune level reporter and can't register water network
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Tu n es pas enregistre dans la liste des rapporteurs du niveau communal"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's check if in that commune a water network with that name is not already
    #registered.
    check_network_registered(args)
    if args['valide']:
        return

    #Let's choose a code of this network
    choose_water_network_code(args)


    WaterNetWork.objects.create(commune = args['the_commune'], water_network_name = args["water_network_name"], reporter = args['the_sender'], length_of_network = 0, water_network_code = args['water_network_code'])
    args["valide"] = True
    args["info_to_contact"] = "Le reseau d eau est bien enregistre. Son code est : "+args['water_network_code']



def record_local_reporter(args):
    '''This function is used to record a colline level reporter'''

    if(args['text'].split('#')[0].upper() == 'RL'):
        #This contact is doing registration not an update
        args['mot_cle'] = "RL"

        check_if_is_colline_level_reporter(args)
        if(args['valide'] is True):
            # This contact is already a colline level reporter and can't do the registration the second time
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous vous etes deja enregistre. Si vous voulez modifier votre enregistrement, envoyer le message de modification d enregistrement"
            return

        # Let's check if the message sent is composed by an expected number of values
        args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
        check_number_of_values(args)
        if not args['valide']:
            return

        # Let's check if names of commune and colline are valid
        args["commune_name"] = args['text'].split('#')[1]
        args["colline_name"] = args['text'].split('#')[2]
        check_commune_colline_names_valide(args)
        if not args['valide']:
            return

        #Let's check if the code of water network is valid
        args["water_network_code"] = args['text'].split('#')[3]
        check_water_network_code_valid(args)
        if not args['valide']:
            return

        args["reporter_name"] =  args['text'].split('#')[3].capitalize()

        #Let's check if the water point name given is unique in that colline
        args["water_point_name"] = args['text'].split('#')[5].upper()
        check_water_point_name_unique_in_colline(args)
        if args['valide']:
            return

        #Let's check if the indicated water point type is valid
        args["water_point_type"] = args['text'].split('#')[6]
        check_water_point_type_exists(args)
        if not args['valide']:
            return

        #Let's check if the value sent for number of households is valid
        args['number_to_check'] = args['text'].split('#')[7]
        args['value_meaning'] = "Nombre de menages"
        check_is_number(args)
        if not args['valide']:
            return
        args['number_of_households'] = int(args['number_to_check'])

        #Let's check if the value sent for number of vulnerable households is valid
        args['number_to_check'] = args['text'].split('#')[8]
        args['value_meaning'] = "Nombre de menages vulnerables"
        check_is_number(args)
        if not args['valide']:
            return
        args['number_of_vulnerable_households'] = int(args['number_to_check'])


        #The value at the position 9 should be yes or no
        if(args['text'].split('#')[9].upper() != "YES" and  args['text'].split('#')[4].upper() != "NO"):
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Pour indiquer si ce point d eau fonctionne ou non, utiliser le mot 'YES' ou 'NO'"
            return
        if(args['text'].split('#')[9].upper() != "YES"):
            args['wp_works'] = True
        else:
            args['wp_works']  = False


        #Let's record the reporter
        reporter = LocalLevelReporter.objects.create(reporter_phone_number = args['phone'], reporter_name = args["reporter_name"], colline = args["concerned_colline"])
        WaterSourceEndPoint.objects.create(water_point_name = args["water_point_name"], water_point_type = args["concerned_water_point_type"], colline = args["concerned_colline"], network = args["concerned_water_network"], reporter = reporter, number_of_households = args['number_of_households'], number_of_vulnerable_households = args['number_of_vulnerable_households'], water_point_functional = args['wp_works'])

        args["info_to_contact"] = "Le point d eau '"+args["water_point_name"]+"' est bien enregistre"

    if(args['text'].split('#')[0].upper() == 'RLM'):
        #This contact is doing an update
        args['mot_cle'] = "RLM"

        #Write hear the code for doing an update



def record_problem_report(args):
    ''' This function is used to record a water point problem '''

    args['mot_cle'] = "RP"

    check_if_is_colline_level_reporter(args)
    if not args['valide']:
        # This contact is not a colline level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs collinaires"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's identify the water point this reporter reports for
    identify_water_point(args)
    if not args['valide']:
        return

    #Let's check if the problem category sent is valid
    args["problem_category"] = args['text'].split('#')[1]
    check_w_p_problem_category_valid(args)
    if not args['valide']:
        return

    #Let's check if the number of days sent is valid
    args["number_of_days"] = args['text'].split('#')[2]
    check_number_of_days_valid(args)
    if not args['valide']:
        return
    args["number_of_days"] = int(args["number_of_days"])

    #Let's check if the action taken sent is valid
    args["action_taken"] = args['text'].split('#')[3]
    check_action_taken_valid(args)
    if not args['valide']:
        return

    #The value at the position 4 should be yes or no
    if(args['text'].split('#')[4].upper() != "YES" and  args['text'].split('#')[4].upper() != "NO"):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Pour indiquer si le probleme est resolu ou pas, utiliser le mot 'YES' ou 'NO'"
        return
    if(args['text'].split('#')[4].upper() != "YES"):
        args['problem_solved'] = False
    else:
        args['problem_solved']  = True


    #The value at the position 4 should be yes or no
    if(args['text'].split('#')[5].upper() != "YES" and  args['text'].split('#')[5].upper() != "NO"):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Pour indiquer s il y a eu des cas de diarrhee ou pas, utiliser le mot 'YES' ou 'NO'"
        return
    if(args['text'].split('#')[5].upper() != "YES"):
        args['is_there_diarrhea_case'] = False
    else:
        args['is_there_diarrhea_case'] = True

    
    wpp_code = WaterPointProblem.objects.filter(water_point = args['concerned_water_point']).count()


    #Let's record the problem report
    WaterPointProblem.objects.create(water_point = args['concerned_water_point'], problem = args["concerned_w_p_pbm_type"], action_taken = args["concerned_action_taken"], days = args["number_of_days"], problem_solved = args['problem_solved'], case_of_diarrhea = args['is_there_diarrhea_case'], wpp_code = wpp_code)

    args['info_to_contact'] = "Le rapport de panne est bien recu. Son code est "+str(wpp_code)


def record_problem_resolution_report(args):
    ''' This function is used to record a water point problem resolution'''

    args['mot_cle'] = "PR"

    check_if_is_colline_level_reporter(args)
    if not args['valide']:
        # This contact is not a colline level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs collinaires"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's identify the water point this reporter reports for
    identify_water_point(args)
    if not args['valide']:
        return

    #Let's check if the value sent for water point problem code is valid
    args['number_to_check'] = args['text'].split('#')[1]
    args['value_meaning'] = "Code de la panne"
    check_is_number(args)
    if not args['valide']:
        return
    args['wpp_code'] = int(args['number_to_check'])


    concerned_wpp = WaterPointProblem.objects.filter(water_point = args['concerned_water_point'], wpp_code = args['wpp_code'])
    if(len(concerned_wpp) > 0):
        concerned_wpp = concerned_wpp[0]
        concerned_wpp.problem_solved = True
        concerned_wpp.save()
        args['info_to_contact'] = "Le rapport de resolution du probleme '"+str(args['wpp_code'])+"' est bien enregistre."
    else:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Il n y a pas de probleme de code '"+str(args['wpp_code'])+"'"




def record_beneficaries_first_month(args):
    ''' This function is used to record beneficiaries at commune level in the first month '''

    args['mot_cle'] = "RPC"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's check if value sent for number of water point commities is valid
    args['number_to_check'] = args['text'].split('#')[1]
    args['value_meaning'] = "Nombre des commites des points d eau"
    check_is_number(args)
    if not args['valide']:
        return
    args['number_of_water_point_committees'] = int(args['number_to_check'])

    #Let's check if value sent for number of households is valid
    args['number_to_check'] = args['text'].split('#')[2]
    args['value_meaning'] = "Nombre de menages"
    check_is_number(args)
    if not args['valide']:
        return
    args['number_of_households'] = int(args['number_to_check'])

    #Let's check if value sent for number of vulnerable households is valid
    args['number_to_check'] = args['text'].split('#')[3]
    args['value_meaning'] = "Nombre de menages vulnerables"
    check_is_number(args)
    if not args['valide']:
        return
    args['number_of_vulnerable_households'] = int(args['number_to_check'])


    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[4]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if the reporting year is valid. It is the year concerned by the report.
    #It's not the year this report is sent. It may be past year or current. Not future.
    args['value_to_check'] = args['text'].split('#')[4]
    args['value_meaning'] = "Annee concernee par le rapport"
    args['lower_limit'] = 2017
    check_is_not_future_year(args)
    if not args['valide']:
        return

    #Let's check if value sent for reporting month is an int
    args['number_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_month'] = int(args['number_to_check'])

    #Let's check if the value sent for reporting month is between 1 and 12
    args['value_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_month_between_1_12(args)
    if not args['valide']:
        return

    #A such report must be sent once per a given commune.
    #Then, let's check if it was not already sent
    wpc_set = NumberOfWaterPointCommittee.objects.filter(commune = args['the_commune'])
    if(len(wpc_set) > 0):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Ce rapport avait ete deja envoye par votre commune."
        return


    NumberOfWaterPointCommittee.objects.create(commune = args['the_commune'], number_of_water_point_committees = args['number_of_water_point_committees'], reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])

    NumberOfHouseHold.objects.create(commune = args['the_commune'], number_of_house_holds = args['number_of_households'], number_of_vulnerable_house_holds = args['number_of_vulnerable_households'], reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])

    args['info_to_contact'] = "Le rapport sur les commites des points d eau et sur les menages est bien recu"


def record_water_sources_points(args):
    ''' This function is used to record number of water sources and water points at commune level in the first month '''

    args['mot_cle'] = "RWP"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    number_of_wp_types = len(args['text'].split('#')) - 3

    for i in range(1,number_of_wp_types):
        args['number_position'] = i
        check_number_is_int(args)
        if not args['valide']:
            break

    if not args['valide']:
        return

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if the reporting year is valid. It is the year concerned by the report.
    #It's not the year this report is sent. It may be past year or current. Not future.
    args['value_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Annee concernee par le rapport"
    args['lower_limit'] = 2017
    check_is_not_future_year(args)
    if not args['valide']:
        return

    #Let's check if value sent for reporting month is an int
    args['number_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_month'] = int(args['number_to_check'])

    #Let's check if the value sent for reporting month is between 1 and 12
    args['value_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_month_between_1_12(args)
    if not args['valide']:
        return

    #A such report must be sent once per a given commune.
    #Then, let's check if it was not already sent
    nwp_set = NumberOfWaterSourceEndPoint.objects.filter(commune = args['the_commune'], report_type = "EXISTING")
    if(len(nwp_set) > 0):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Ce rapport avait ete deja envoye par votre commune."
        return

    for i in range(1,number_of_wp_types+1):
        wpt_set = WaterPointType.objects.filter(priority = i)
        number = args['text'].split('#')[i]
        if(len(wpt_set) > 0):
            wpt = wpt_set[0]
            NumberOfWaterSourceEndPoint.objects.create(commune = args['the_commune'], water_point_type = wpt, existing_number = number, reporting_year = args['reporting_year'], reporting_month = args['reporting_month'], report_type = "EXISTING")
        else:
            args['valide'] = False
            args['info_to_contact'] = "Erreur admin. Creer les types de points d eau."
            break

    if args['valide']:
        args['info_to_contact'] = "Le rapport concernant les points d eau existants est bien recu"




def record_additional_water_sources_points(args):
    ''' This function is used to record number of additional water sources and water points at commune level '''

    args['mot_cle'] = "RWA"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    number_of_wp_types = len(args['text'].split('#')) - 3

    for i in range(1,number_of_wp_types):
        args['number_position'] = i
        check_number_is_int(args)
        if not args['valide']:
            break

    if not args['valide']:
        return

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if the reporting year is valid. It is the year concerned by the report.
    #It's not the year this report is sent. It may be past year or current. Not future.
    args['value_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Annee concernee par le rapport"
    args['lower_limit'] = 2017
    check_is_not_future_year(args)
    if not args['valide']:
        return

    #Let's check if value sent for reporting month is an int
    args['number_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_month'] = int(args['number_to_check'])

    #Let's check if the value sent for reporting month is between 1 and 12
    args['value_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_month_between_1_12(args)
    if not args['valide']:
        return


    for i in range(1,number_of_wp_types+1):
        wpt_set = WaterPointType.objects.filter(priority = i)
        number = args['text'].split('#')[i]
        if(len(wpt_set) > 0):
            wpt = wpt_set[0]
            NumberOfWaterSourceEndPoint.objects.create(commune = args['the_commune'], water_point_type = wpt, additional_number = number, reporting_year = args['reporting_year'], reporting_month = args['reporting_month'], report_type = "ADDITIONAL")
        else:
            args['valide'] = False
            args['info_to_contact'] = "Erreur admin. Contacter l administrateur de ce systeme"
            break

    if args['valide']:
        args['info_to_contact'] = "Le rapport concernant les nouveaux points d eau est bien recu"



def record_functional_water_sources_points(args):
    ''' This function is used to record number of functional water sources and water points at commune level'''

    args['mot_cle'] = "RWF"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    number_of_wp_types = len(args['text'].split('#')) - 3

    for i in range(1,number_of_wp_types):
        args['number_position'] = i
        check_number_is_int(args)
        if not args['valide']:
            break

    if not args['valide']:
        return

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if the reporting year is valid. It is the year concerned by the report.
    #It's not the year this report is sent. It may be past year or current. Not future.
    args['value_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Annee concernee par le rapport"
    args['lower_limit'] = 2017
    check_is_not_future_year(args)
    if not args['valide']:
        return

    #Let's check if value sent for reporting month is an int
    args['number_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_month'] = int(args['number_to_check'])

    #Let's check if the value sent for reporting month is between 1 and 12
    args['value_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_month_between_1_12(args)
    if not args['valide']:
        return


    for i in range(1,number_of_wp_types+1):
        wpt_set = WaterPointType.objects.filter(priority = i)
        number = args['text'].split('#')[i]
        if(len(wpt_set) > 0):
            wpt = wpt_set[0]
            NumberOfWaterSourceEndPoint.objects.create(commune = args['the_commune'], water_point_type = wpt, functional_number = number, reporting_year = args['reporting_year'], reporting_month = args['reporting_month'], report_type = "FUNCTIONAL")
        else:
            args['valide'] = False
            args['info_to_contact'] = "Erreur"
            break

    if args['valide']:
        args['info_to_contact'] = "Le rapport concernant le fonctionnement des points d eau est bien recu"




def record_annual_budget(args):
    ''' This function is used to record annual budget '''

    args['mot_cle'] = "RBB"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's check if value sent for budget amount is an int
    args['number_to_check'] = args['text'].split('#')[1]
    args['value_meaning'] = "Budget annuel"
    check_is_number(args)
    if not args['valide']:
        return
    args['annual_budget'] = int(args['number_to_check'])

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[2]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_year(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if this report is not already given
    budget_set = ExpectedBudgetExpenditureAndAnnualBudget.objects.filter(commune = args['the_commune'], reporting_year = args['reporting_year'])
    if(len(budget_set) > 0):
        one_budget_row = budget_set[0]
        if(one_budget_row.annual_badget):
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Ce rapport avait ete deja envoye par votre commune."
            return
        else:
            args['valide'] = True
            one_budget_row.annual_badget = args['annual_budget']
            one_budget_row.save()
            args['info_to_contact'] = "Le rapport de budget annuel est bien recu"
            return

    ExpectedBudgetExpenditureAndAnnualBudget.objects.create(commune = args['the_commune'], annual_badget = args['annual_budget'], reporting_year = args['reporting_year'])


    args['info_to_contact'] = "Le rapport de budget annuel est bien recu"



def record_expected_expenditure(args):
    ''' This function is used to record expected expenditure '''

    args['mot_cle'] = "RBE"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's check if value sent for expected annual expenditure is an int
    args['number_to_check'] = args['text'].split('#')[1]
    args['value_meaning'] = "Prevision des depenses annuelles"
    check_is_number(args)
    if not args['valide']:
        return
    args['expected_annual_expenditure'] = int(args['number_to_check'])

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[2]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_year(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if this report is not already given
    budget_set = ExpectedBudgetExpenditureAndAnnualBudget.objects.filter(commune = args['the_commune'], reporting_year = args['reporting_year'])
    if(len(budget_set) > 0):
        one_budget_row = budget_set[0]
        if(one_budget_row.expected_annual_expenditure):
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Ce rapport avait ete deja envoye par votre commune."
            return
        else:
            args['valide'] = True
            one_budget_row.expected_annual_expenditure = args['expected_annual_expenditure']
            one_budget_row.save()
            args['info_to_contact'] = "Le rapport de prevision des depenses annuelles est bien recu"
            return

    ExpectedBudgetExpenditureAndAnnualBudget.objects.create(commune = args['the_commune'], expected_annual_expenditure = args['expected_annual_expenditure'], reporting_year = args['reporting_year'])


    args['info_to_contact'] = "Le rapport de prevision des depenses annuelles est bien recu"



def record_income_money(args):
    ''' This function is used to record income money '''

    args['mot_cle'] = "RCI"
    
    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's check if the value sent for amount collected is an int
    args['number_to_check'] = args['text'].split('#')[1]
    args['value_meaning'] = "Montant collecte"
    check_is_number(args)
    if not args['valide']:
        return
    args['amount_collected'] = int(args['number_to_check'])

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[2]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_year(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if value sent for reporting month is an int
    args['number_to_check'] = args['text'].split('#')[3]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_month'] = int(args['number_to_check'])

    #Let's check if the value sent for reporting month is between 1 and 12
    args['value_to_check'] = args['text'].split('#')[3]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_month_between_1_12(args)
    if not args['valide']:
        return


    monthly_income_set = MonthlyIncome.objects.filter(commune = args['the_commune'], reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])

    if(len(monthly_income_set) > 0):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Votre commune avait deja donne le montant collecte pendant cette periode"
        return
    else:
        MonthlyIncome.objects.create(commune = args['the_commune'], total_income = args['amount_collected'], reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])
        args['info_to_contact'] = "Le rapport de montant collecte est bien recu"


def record_expenditure(args):
    ''' This function is used to record expenditure '''

    args['mot_cle'] = "RCI"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's check if the value sent for Amount spent on Services and Repairs is an int
    args['number_to_check'] = args['text'].split('#')[1]
    args['value_meaning'] = "Montant depense pour les reparations"
    check_is_number(args)
    if not args['valide']:
        return
    args['amount_spend_on_repairs'] = int(args['number_to_check'])


    #Let's check if the value sent for Amount spent on Equipment and logistics is an int
    args['number_to_check'] = args['text'].split('#')[2]
    args['value_meaning'] = "Montant depense pour les Equipments"
    check_is_number(args)
    if not args['valide']:
        return
    args['amount_spend_on_equipments'] = int(args['number_to_check'])


    #Let's check if the value sent for Amount spent on Salaries is an int
    args['number_to_check'] = args['text'].split('#')[3]
    args['value_meaning'] = "Montant depense pour les salaires"
    check_is_number(args)
    if not args['valide']:
        return
    args['amount_spend_on_salaries'] = int(args['number_to_check'])


    #Let's check if the Amount spent on Administrative costs is an int
    args['number_to_check'] = args['text'].split('#')[4]
    args['value_meaning'] = "Montant depense pour l administration"
    check_is_number(args)
    if not args['valide']:
        return
    args['amount_spend_on_administrations'] = int(args['number_to_check'])

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_year(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if value sent for reporting month is an int
    args['number_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_month'] = int(args['number_to_check'])

    #Let's check if the value sent for reporting month is between 1 and 12
    args['value_to_check'] = args['text'].split('#')[6]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_month_between_1_12(args)
    if not args['valide']:
        return

    expenditure_set = MonthlyExpenditure.objects.filter(commune = args['the_commune'], reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])

    if len(expenditure_set) > 0:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Votre commune avait deja donne le rapport des depenses pour cette periode"
        return
    else:
        number_of_expensy_types = len(args['text'].split('#')) - 3

        for i in range(1,number_of_expensy_types+1):
            expensy_type_set = ExpenditureCategory.objects.filter(priority = i)
            number = int(args['text'].split('#')[i])
            if(len(expensy_type_set) > 0):
                exp_t = expensy_type_set[0]
                MonthlyExpenditure.objects.create(commune = args['the_commune'], expenditure = exp_t, expenditure_amount = number, reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])
            else:
                args['valide'] = False
                args['info_to_contact'] = "Erreur admin. Contacter l administrateur de ce systme."
                break

    if args['valide']:
        args['info_to_contact'] = "Le rapport concernant les depenses est bien recu"



def record_network_problem(args):
    ''' This function is used to record network problems '''

    args['mot_cle'] = "RNP"

    check_if_is_commune_level_reporter(args)
    if not args['valide']:
        # This contact is not a commune level reporter
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre dans la liste des rapporteurs communaux"
        return

    # Let's check if the message sent is composed by an expected number of values
    args["expected_number_of_values"] = getattr(settings, 'EXPECTED_NUMBER_OF_VALUES', '')[args['message_type']]
    check_number_of_values(args)
    if not args['valide']:
        return

    #Let's check if the value sent for number of network problems is an int
    args['number_to_check'] = args['text'].split('#')[1]
    args['value_meaning'] = "Nombre de pannes sur le reseau"
    check_is_number(args)
    if not args['valide']:
        return
    args['nb_de_pannes_sur_le_reseau'] = int(args['number_to_check'])

    #Let's check if the value sent for days the problem lasted is an int
    args['number_to_check'] = args['text'].split('#')[2]
    args['value_meaning'] = "Nombre de jours que le reseau est en panne"
    check_is_number(args)
    if not args['valide']:
        return
    args['nb_de_jours_reseau_en_panne'] = int(args['number_to_check'])

    #Let's check if the network type sent is valid
    args['network_problem_type_code'] = args['text'].split('#')[3]
    check_water_network_problem_type(args)
    if not args['valide']:
        return

    #Let's check if value sent for reporting year is an int
    args['number_to_check'] = args['text'].split('#')[4]
    args['value_meaning'] = "Annee concernee par le rapport"
    check_is_year(args)
    if not args['valide']:
        return
    args['reporting_year'] = int(args['number_to_check'])

    #Let's check if value sent for reporting month is an int
    args['number_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_is_number(args)
    if not args['valide']:
        return
    args['reporting_month'] = int(args['number_to_check'])

    #Let's check if the value sent for reporting month is between 1 and 12
    args['value_to_check'] = args['text'].split('#')[5]
    args['value_meaning'] = "Moi concerne par le rapport"
    check_month_between_1_12(args)
    if not args['valide']:
        return



    water_network_problem_set = NumberOfWaterNetworkProblems.objects.filter(commune = args['the_commune'], reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])

    if len(water_network_problem_set) > 0:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Votre commune avait deja donne le rapport des problemes des reseaux d eau pour cette periode"
        return

    NumberOfWaterNetworkProblems.objects.create(commune = args['the_commune'], most_frequent_water_network_problem_type = args["concerned_w_network_pbm_type"], number_of_water_network_problems = args['nb_de_pannes_sur_le_reseau'], number_of_days = args['nb_de_jours_reseau_en_panne'], reporting_year = args['reporting_year'], reporting_month = args['reporting_month'])
    args['info_to_contact'] = "Le rapport concernant les problemes des reseaux d eau est bien recu"


