from __future__ import print_function
from botocore.vendored import requests
from datetime import datetime
import logging

def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return get_help() #provide functionality desc
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event) #execute command

def on_intent(event):
    intent = event['request']['intent']
    intent_name = event['request']['intent']['name']
    print('on_intent, session: ')
    print(event['session'])

    if intent_name == "GetTrainTimes":
        return get_train_time(event)
    elif intent_name == "getBusTimes":
        return get_bus_time(event)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help()
    elif intent_name == "AMAZON.CancelIntent":
        return nothing()
    elif intent_name == "AMAZON.StopIntent":
        return nothing()

def get_train_time(event):
    train_times = IrishRailRTPI()
    origin = input('origin: ')
    #destination = raw_input('destination: ')
    dir = input('direction: ')
    data = json.dumps(train_times.get_station_by_name(origin,num_minutes=30), indent=4, sort_keys=True)
    resp = json.loads(data)

    for i in range(len(resp)):
        dict_data = resp[i]
        if dict_data['direction']==dir: #filter out by direction
            #print(dict_data)
            to_say = "the next "+dir+" train is in"+dict_data['due_in_mins']+"mins"
            return say_duration(to_say)

def get_bus_time(event):
    route = input('Enter route number: ')
    stop_number = input('Enter stop number: ')
    g = db.RtpiApi(user_agent='test')
    bus_times = g.rtpi(stop_number, route)
    #print(my_stop.timestamp)
    to_say = "the next"+route+"bus is in in"+bus_times.results[0]['duetime']+"mins"
    return say_duration(to_say)

def build_speechlet_response(title, output, reprompt_text, shouldEndSession):
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

def nothing():
    retutn(build_response({}))

def get_help():
    speech_output = "welcome to transport times"
    card_title = "transport times error"
    shouldEndSession = False
    return build_response(build_speechlet_response(card_title, speed_output, None, shouldEndSession))

def say_duration(duration):
    speech_output = duration
    card_title = 'Transport times'
    should_end_session = True
    return build_response(build_speechlet_response(card_title, speech_output, None, should_end_session))
