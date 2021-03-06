from __future__ import print_function
import db
from ir import IrishRailRTPI
import json
import string

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# skill behaviour
def get_test_response():
    session_attributes = {}
    card_title = "Test"
    speech_output = "This is a test message"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    #start up message
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Are you getting the bus or the train?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "which transport service are you looking for?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

#train times from ir.py file
def get_train_time(intent):
    session_attributes = {}
    card_title = "train times"
    speech_output = ""
    train_times = IrishRailRTPI()
    origin = intent['slots']['origin']['value']
    destination = intent['slots']['direction']['value']
    data = json.dumps(train_times.get_station_by_name(origin, destination), indent=4, sort_keys=False)
    resp = json.loads(data)
    try:
        for i in range(len(resp)):  #len(resp) returns the amount of dictionaries
            print("{} : {}".format(i,resp[i]['destination']))
            des = resp[i]['destination']
            if des.lower()==destination.lower(): #filter out by direction and make into lower case
                due_time = resp[i]["due_in_mins"]
                if due_time == "Due":
                    speech_output = "The next "+destination+" is due now"
                else:
                    speech_output = "the next "+destination+" train is in "+due_time+" minutes"
                break
    
    except:
        speech_output = "There were no trains found for your request. Please try asking again"
    reprompt_text = "reprompt text"
    should_end_session = True

    return build_response(session_attributes,build_speechlet_response(
        card_title, speech_output,reprompt_text, should_end_session
        ))

#get the bus times from db.py file
def get_bus_time(intent):
    card_title="Bus times"
    session_attributes={}

    route = intent['slots']['RouteName']['value']
    form_route = route.translate({ord(c): None for c in string.whitespace}) #remove whitespaces
    stop_number = int(intent['slots']['stopNumber']['value'])
    g = db.RtpiApi(user_agent='test')
    bus_times=g.rtpi(stop_number,form_route)
    try:
        next_bus = bus_times.results[0]['duetime']
        
        if next_bus == "Due":
            speech_output = "the next "+form_route+" bus calling at stop "+str(stop_number)+" is due now "
        else:
            speech_output="the next "+form_route+" bus calling at stop: "+str(stop_number)+" is in "+str(next_bus)+ " minutes"

    except:
        speech_output = "there are currently no such buses at the requested stop"
        
    reprompt_text="please tell me what you want. this is a reprompt"
    should_end_session=True

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a nice day!"
    # True setting ends ends the session
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# events

def on_session_started(session_started_request, session):
    #called when session starts
    # Add additional code here as needed
    pass

def on_launch(launch_request, session):
    #Called when the user launches the skill without specifying what they want
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    #Called when the user specifies an intent for this skill

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']


    if intent_name == "test":
        return get_test_response()
    elif intent_name == "GetTrainTimes":
        return get_train_time(intent)
    elif intent_name == "GetBusTimes":
        return get_bus_time(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    #when user ends session
    print("on_session_ended requestId=" + session_ended_request['requestId'] +", sessionId=" + session['sessionId'])


# Handler

def lambda_handler(event, context):
    #Route the incoming request based on type (LaunchRequest, IntentRequest, etc.)

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
