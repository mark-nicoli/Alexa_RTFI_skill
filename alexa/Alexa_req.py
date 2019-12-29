import logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_core.model.ui import SimpleCard
from ask_sdk_model import Response

import requests

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest")) #what kind of request
def launch_request_handler(handler_input):
    speech = "Hi, Welcome to Transport Times"
    qtext = "what service would you like to use"
    handler_input.response_builder.speak(speech+""+qtext).ask(qtext)

    return handler_input.response_builder.response

@sb.request_handler(can_handle_func=is_intent_name("GetTransportTimesIntent"))
def next_train(handler_input):
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
            return ('the next {} train is in {} mins'.format(dir, dict_data['due_in_mins']))
