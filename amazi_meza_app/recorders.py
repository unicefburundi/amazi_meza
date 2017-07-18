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

        #Let's record the reporter
        reporter = LocalLevelReporter.objects.create(reporter_phone_number = args['phone'], reporter_name = args["reporter_name"], colline = args["concerned_colline"])
        WaterSourceEndPoint.objects.create(water_point_name = args["water_point_name"], water_point_type = args["concerned_water_point_type"], colline = args["concerned_colline"], network = args["concerned_water_network"], reporter = reporter)

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

    #The value at the position 4 should be yes or not
    if(args['text'].split('#')[4].upper() != "YES" and  args['text'].split('#')[4].upper() != "NO"):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Pour indiquer si le probleme est resolu ou pas, utiliser le mot 'YES' ou 'NO'"
        return
    if(args['text'].split('#')[4].upper() != "YES"):
        args['problem_solved'] = True
    else:
        args['problem_solved']  = False


    #The value at the position 4 should be yes or not
    if(args['text'].split('#')[5].upper() != "YES" and  args['text'].split('#')[5].upper() != "NO"):
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Pour indiquer s il y a eu des cas de diarrhee ou pas, utiliser le mot 'YES' ou 'NO'"
        return
    if(args['text'].split('#')[5].upper() != "YES"):
        args['is_there_diarrhea_case'] = True
    else:
        args['is_there_diarrhea_case'] = False


    #Let's record the problem report
    WaterPointProblem.objects.create(water_point = args['concerned_water_point'], problem = args["concerned_w_p_pbm_type"], action_taken = args["concerned_action_taken"], days = args["number_of_days"], problem_solved = args['problem_solved'], case_of_diarrhea = args['is_there_diarrhea_case'])

    args['info_to_contact'] = "Le rapport est bien recu"