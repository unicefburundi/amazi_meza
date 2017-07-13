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
    ''' This function checks if the contact who sent the current message is a CHW '''
    args['valide'] = False
    concerned_reporter = CommuneLevelReporters.objects.filter(reporter_phone_number = args['phone'])
    if len(concerned_reporter) > 0:
        args['valide'] = True
        args['reporter_category'] == "C"
        one_concerned_reporter = concerned_reporter[0]

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

    args['the_sender'] = concerned_reporter
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

        # Let's check if the code of CDS is valid
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


def record_local_reporter(args):
    '''This function is used to record a colline level reporter'''
    pass
