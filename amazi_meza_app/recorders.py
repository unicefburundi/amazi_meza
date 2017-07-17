from public_administration_structure_app.models import *
from amazi_meza_app.models import *

import datetime
from django.conf import settings

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

        # Let's check if the name of the commune is valid
        args["commune_code"] = args['text'].split('#')[1]
        check_commune_exists(args)
        if not args['valide']:
            return



    if(args['text'].split('#')[0].upper() == 'RLM'):
        #This contact is doing an update
        args['mot_cle'] = "RLM"

        #Write hear the code for doing an update
