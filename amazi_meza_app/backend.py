from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
import re
from django.conf import settings
import urllib
from models import *
from recorders import *



def eliminate_unnecessary_spaces(arg):
    '''This function eliminate unnecessary spaces in the incoming message'''
    the_incoming_message = arg['text']

    # Messages from RapidPro comes with spaces replaced by '+'
    # Let's replace those '+' (one or more) by one space
    the_new_message = re.sub('[+]+',' ',the_incoming_message)

    #  Find any comma
    the_new_message = urllib.unquote_plus(the_new_message)    

    # Let's eliminate spaces at the begining and the end of the message
    the_new_message = the_new_message.strip()
    arg['text'] = the_new_message


def identify_message(arg):
    ''' This function identifies which kind of message this message is. '''
    incoming_prefix = arg['text'].split('#')[0].upper()
    if arg['text'].split('#')[0].upper() in getattr(settings,'KNOWN_PREFIXES',''):
        # Prefixes and related meanings are stored in the dictionary "KNOWN_PREFIXES"
        arg['message_type'] = getattr(settings,'KNOWN_PREFIXES','')[incoming_prefix]
    	arg['info_to_contact'] = "Le SMS est reconnu"
    else:
        arg['message_type'] = "UNKNOWN_MESSAGE"
        arg['info_to_contact'] = "Le SMS n est pas reconnu"

@csrf_exempt
@json_view
def handel_rapidpro_request(request):
	'''This function receives requests sent by RapidPro.
	This function send json data to RapidPro as a response.'''
	#We will put all data sent by RapidPro in this variable
	incoming_data = {}

	#Two couples of variable/value are separated by &
	#Let's put couples of variable/value in a list called 'list_of_data'
	list_of_data = request.body.split("&")

	#Let's put all the incoming data in the dictionary 'incoming_data'
	for couple in list_of_data:
		incoming_data[couple.split("=")[0]] = couple.split("=")[1]

	#Let's assume that the incoming data is valid
	incoming_data['valide'] = True
	incoming_data['info'] = "The default information."

	#Because RapidPro sends the contact phone number by replacing "+" by "%2B"
	#let's rewrite the phone number in a right way.
	incoming_data['phone'] = incoming_data['phone'].replace("%2B","+")

	#Let's instantiate the variable this function will return
	response = {}

	#Let's eliminate unnecessary spaces in the incoming message
	eliminate_unnecessary_spaces(incoming_data)
	
	#Let's check which kind of message this message is.
	identify_message(incoming_data)

	if(incoming_data['message_type']=='UNKNOWN_MESSAGE'):
		#Let's check if this contact is confirming his phone number
		#It means that he has an already created session
		response['ok'] = False
		response['info_to_contact'] = "Le mot qui commence le message envoye n est pas reconnu par le systeme"
		'''check_session(incoming_data)
		if not(incoming_data['has_session']):
			#This contact doesn't have an already created session
			response['ok'] = False
			response['info_to_contact'] = "Le mot qui commence votre message n est pas reconnu par le systeme. Reenvoyez votre message en commencant par un mot cle valide."
			return response
		else:
			#This contact is confirming the phone number of his supervisor
			complete_registration(incoming_data)
			#response['ok'] = False
			response['ok'] = incoming_data['valide']
			response['info_to_contact'] = incoming_data['info_to_contact']
			return response'''



	if(incoming_data['message_type']=='LOCAL_SELF_REGISTRATION' or incoming_data['message_type']=='LOCAL_SELF_REGISTRATION_M'):
		#The contact who sent the current message is doing self registration  in the group of reporters
		#L is local reporter
		incoming_data['reporter_category'] = "L"
		record_local_reporter(incoming_data)
		
	if(incoming_data['message_type']=='COMMUNE_LEVEL_SELF_REGISTRATION' or incoming_data['message_type']=='COMMUNE_LEVEL_SELF_REGISTRATION_M'):
		#The contact who sent the current message is doing self registration  in the group of reporters
		#C is commune level reporter
		incoming_data['reporter_category'] = "C"
		record_commune_level_reporter(incoming_data)

	if(incoming_data['message_type']=='RECORD_NETWORK' or incoming_data['message_type']=='RECORD_NETWORK_M'):
		#The contact who sent this message is registering a water network
		record_water_network(incoming_data)

	if incoming_data['valide'] :
		#The message have been recorded
		response['ok'] = True
	else:
		#The message haven't been recorded
		response['ok'] = False


	response['info_to_contact'] = incoming_data['info_to_contact']

	return response