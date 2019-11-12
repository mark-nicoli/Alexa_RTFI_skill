<<<<<<< HEAD
from __future__ import print_function
from botocore.vendored import requests
from datetime import datetime
=======
>>>>>>> 948c14344f0070190f8195ef865042a48a3cd758
import logging
import ask_sdk_core.utils as ask_utils

<<<<<<< HEAD
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
=======
import json
from ir import IrishRailRTPI
import db

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Would you like train or bus times?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class GetTrainTimesHandler(AbstractRequestHandler):
    """Handler for train times Intent."""

    """

    def rail_time():
        train_times = IrishRailRTPI()
        origin = input('origin: ')
        #destination = raw_input('destination: ')
        dir = input('direction: ')
        data = json.dumps(train_times.get_station_by_name(origin,num_minutes=30), indent=4, sort_keys=True)
        resp = json.loads(data)

        for i in range(len(resp)):
            dict_data = resp[i]
            if dict_data['direction']==dir: #filter out by direction
                return ('the next {} train is in {} mins'.format(dir, dict_data['due_in_mins']))


    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetTrainTimes")(handler_input)

    def handle():
        train_times = IrishRailRTPI()
        origin = "Maynooth"
        #destination = raw_input('destination: ')
        direction = "southbound"
        data = json.dumps(train_times.get_station_by_name(origin,num_minutes=30), indent=4, sort_keys=True)
        resp = json.loads(data)

        for i in range(len(resp)):
            dict_data = resp[i]
            if dict_data['direction']==direction: #filter out by direction
                time = dict_data['due_in_mins']
                alexa_resp = "the next"+direction+"train is in"+time+"mins"
                alexa_ask = "wanna hear bus times?"

        return(
            handler_input.response_builder
            .speak(alexa_resp)
            .ask(alexa_ask)
        )


class GetBusTimesHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetBusTimes")(handler_input)

    def handle(self, handler_input):
        route_speech = "which route are you looking for?"
        slots = handler_input.request_envelope.request.intent.slots
        route = (slots["RouteNumber"].value)
        stop_number = 4825
        g = db.RtpiApi(user_agent='test')
        bus_times = g.rtpi(stop_number, route)
        if bus_times.results[0]['duetime'] == 'Due':
            speak_output = "The bus is due now"
        else:
            speak_output = "The next bus is in "+bus_times.results[0]['duetime']+" minutes"
        
        return (
            handler_input.response_builder
            .speak(route_speech)
            .speak(speak_output)
            .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(GetTrainTimesHandler())
sb.add_request_handler(GetBusTimesHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
>>>>>>> 948c14344f0070190f8195ef865042a48a3cd758
