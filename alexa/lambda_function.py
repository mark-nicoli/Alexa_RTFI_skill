from __future__ import print_function
import db
from ir import IrishRailRTPI
import json

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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
    speech_output = "welcome to transport times. Would you like train or bus times?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I don't know if you heard me, welcome to your custom alexa application!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

# train times from ir api
def get_train_time(intent):
    session_attributes = {}
    card_title = "train times"

    '''
        input type{
            pearse station: Dublin pearse
            connolly: Dublin Connolly
        }
        
    '''
    
    train_times = IrishRailRTPI()
    origin = intent['slots']['origin']['value']
    destination = intent['slots']['direction']['value']
    data = json.dumps(train_times.get_station_by_name(origin,destination), indent=4, sort_keys=True)
    resp = json.loads(data)
    speech_output = ''

    #for i in range(len(resp)):
    dict_data = resp[0]
    if dict_data['destination'].lower()==destination.lower(): #filter out by direction and make into lower case
        if dict_data['due_in_mins'] == 'Due':
            speech_output = "The train is due now"
        else:
            speech_output = "the next "+destination+" train is in "+dict_data['due_in_mins']+" mins"

    reprompt_text = "reprompt text"
    should_end_session = False

    return build_response(session_attributes,build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session
        ))

#get the bus times from db.py file
def get_bus_time(intent):
    card_title="Bus times"
    session_attributes={}

    route = intent['slots']['RouteName']['value']
    #route=37
    #stop number = 4825
    stop_number = int(intent['slots']['stopNumber']['value'])
    g = db.RtpiApi(user_agent='test')
    bus_times=g.rtpi(stop_number,route)
    next_bus = bus_times.results[0]['duetime']
    speech_output="the next "+route+" bus callin at stop: "+str(stop_number)+" is in "+str(next_bus)+" minutes"
    reprompt_text="please tell me what you want. this is a reprompt"
    should_end_session=False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. "\
                    "Have a nice day! "
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
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

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
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# Handler

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


'''
{
	"version": "1.0",
	"session": {
		"new": false,
		"sessionId": "amzn1.echo-api.session.e5267bf0-f77e-4025-b1f9-5f515b4a5737",
		"application": {
			"applicationId": "amzn1.ask.skill.5c6dcd7c-95cb-44fe-9d69-733d97006734"
		},
		"user": {
			"userId": "amzn1.ask.account.AECQEILRISXDPJWYE6U5UWCTTXRZLURTMBY5Y7XFHLULTXPS6ZWWJSCT6ABEQ46LO2QHVALY4S7C22RY5B4P4PVCMKXDI2UGVMGQGPFODNDCNQVKNH6QN3LXFEOAFQXYJ4NF33PYTZDA7RF4SZCNMZLHUOZXRS4VOT2FXYBACJODHFUXYP4NUN3OMP2AWXP2WBFTD3EJ6NXI3WI"
		}
	},
	"context": {
		"System": {
			"application": {
				"applicationId": "amzn1.ask.skill.5c6dcd7c-95cb-44fe-9d69-733d97006734"
			},
			"user": {
				"userId": "amzn1.ask.account.AECQEILRISXDPJWYE6U5UWCTTXRZLURTMBY5Y7XFHLULTXPS6ZWWJSCT6ABEQ46LO2QHVALY4S7C22RY5B4P4PVCMKXDI2UGVMGQGPFODNDCNQVKNH6QN3LXFEOAFQXYJ4NF33PYTZDA7RF4SZCNMZLHUOZXRS4VOT2FXYBACJODHFUXYP4NUN3OMP2AWXP2WBFTD3EJ6NXI3WI"
			},
			"device": {
				"deviceId": "amzn1.ask.device.AEUYN77FD4J4EDRYDU5G4I6GNUV26LVVDVITP4UPYVGNQLH5ZQ337NZCBVBP667QDUQEOVZ6SMMTIEHOULMXOG32O52QLX23LY5VUF6Y3P6KKLD5JEWKN4VJU524AUOKETQJCMUNJBJNKNA4BAWNUFVILAMKGFXELHQCSS4BH3NJG7M6YCCL6",
				"supportedInterfaces": {}
			},
			"apiEndpoint": "https://api.eu.amazonalexa.com",
			"apiAccessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJhdWQiOiJodHRwczovL2FwaS5hbWF6b25hbGV4YS5jb20iLCJpc3MiOiJBbGV4YVNraWxsS2l0Iiwic3ViIjoiYW16bjEuYXNrLnNraWxsLjVjNmRjZDdjLTk1Y2ItNDRmZS05ZDY5LTczM2Q5NzAwNjczNCIsImV4cCI6MTU4MDQ3MTEyNCwiaWF0IjoxNTgwNDcwODI0LCJuYmYiOjE1ODA0NzA4MjQsInByaXZhdGVDbGFpbXMiOnsiY29udGV4dCI6IkFBQUFBQUFBQVFCOGlwb29FOUFpK1VTTy9sYVJtNEFES3dFQUFBQUFBQURHYmpvRWVNL1VzTkc5NXpnNi9XYXRWMTkxVmt2UEJMdnRRS0o4VDg2cUNObUczSFc0MjQzcTZiTS9GbVRSWEI2RCtFZ2d6c21UZUQzZnpEanNzNWFFczQ1NDhiaFdhWUNtZGZOR1pjRDFrY2NrNlJ5QjJvSWN3ZGdiTlNWMVFWbVFmSjN4aFFLSXpiaDJKcFU2dSt2dGhYSG5od2RWT0k4clJoTE1rMTBFd1BCblREZ1hlMVVrakIxbDJJMWQ0NUs3ZUoxVlV6Y3E5aUovc2ZHdHQvMWtUYlpuNmJxM2xTY0ZPQjhqczRmd0VHTUJGZDNIVUZ5SEVBb2xzN1JJYkVUbWhIcjNtKzlsTWl0alRLLzU1WHBqbzdzbzN1KzJhVWNMZjlVaU8zaHNhMXF0ME9kU2ZpeisvdDRLenNVTFRrcHBJTXIwTk5NcS84UW9DRTYzWTBxQnhnU3Qybm01MVRSNllKVSs4N2pPekVMSlYrTzZUNWNUWFhxODVFOVozeDRodk9oN3U2ampHTXFoRXc9PSIsImNvbnNlbnRUb2tlbiI6bnVsbCwiZGV2aWNlSWQiOiJhbXpuMS5hc2suZGV2aWNlLkFFVVlONzdGRDRKNEVEUllEVTVHNEk2R05VVjI2TFZWRFZJVFA0VVBZVkdOUUxINVpRMzM3TlpDQlZCUDY2N1FEVVFFT1ZaNlNNTVRJRUhPVUxNWE9HMzJPNTJRTFgyM0xZNVZVRjZZM1A2S0tMRDVKRVdLTjRWSlU1MjRBVU9LRVRRSkNNVU5KQkpOS05BNEJBV05VRlZJTEFNS0dGWEVMSFFDU1M0QkgzTkpHN002WUNDTDYiLCJ1c2VySWQiOiJhbXpuMS5hc2suYWNjb3VudC5BRUNRRUlMUklTWERQSldZRTZVNVVXQ1RUWFJaTFVSVE1CWTVZN1hGSExVTFRYUFM2WldXSlNDVDZBQkVRNDZMTzJRSFZBTFk0UzdDMjJSWTVCNFA0UFZDTUtYREkyVUdWTUdRR1BGT0RORENOUVZLTkg2UU4zTFhGRU9BRlFYWUo0TkYzM1BZVFpEQTdSRjRTWkNOTVpMSFVPWlhSUzRWT1QyRlhZQkFDSk9ESEZVWFlQNE5VTjNPTVAyQVdYUDJXQkZURDNFSjZOWEkzV0kifX0.gWMN5PBNOdw9cnn6ySAe05Wn2Eo7388AC9tVQTKYDzh08mtXpTmWvB-dX7_cLLqBA95LZVYPxhHtbpXnN4UafwQwTY3TQX8L9WGYc4MIkKKc_lBoLD-6Pha4Pk14I_-dBcEf76hHmd5DBwNQzJBTs-YmlsjkTQi3cn_626WwVnRT-ihY3zXOtAn7HT6hP0MYegQKn7ZFVC22y0uwAc7byW2T-6LjHpqNmB2Ob-KM50nPqiLBHi3dJPU7oQPb7RPYiYt37zn4nUxxXYZp1II2MD3RodQl-ut-SH7PzRXhXPvdBTcFBxr8tAR3f5TNLrmzXDiT5DR39Xz4vJno5W-xkA"
		},
		"Viewport": {
			"experiences": [
				{
					"arcMinuteWidth": 246,
					"arcMinuteHeight": 144,
					"canRotate": false,
					"canResize": false
				}
			],
			"shape": "RECTANGLE",
			"pixelWidth": 1024,
			"pixelHeight": 600,
			"dpi": 160,
			"currentPixelWidth": 1024,
			"currentPixelHeight": 600,
			"touch": [
				"SINGLE"
			],
			"video": {
				"codecs": [
					"H_264_42",
					"H_264_41"
				]
			}
		},
		"Viewports": [
			{
				"type": "APL",
				"id": "main",
				"shape": "RECTANGLE",
				"dpi": 160,
				"presentationType": "STANDARD",
				"canRotate": false,
				"configuration": {
					"current": {
						"video": {
							"codecs": [
								"H_264_42",
								"H_264_41"
							]
						},
						"size": {
							"type": "DISCRETE",
							"pixelWidth": 1024,
							"pixelHeight": 600
						}
					}
				}
			}
		]
	},
	"request": {
		"type": "IntentRequest",
		"requestId": "amzn1.echo-api.request.4f07aefc-ec82-4f67-8bdb-d4c163dcfd3e",
		"timestamp": "2020-01-31T11:40:24Z",
		"locale": "en-GB",
		"intent": {
			"name": "GetTrainTimes",
			"confirmationStatus": "NONE",
			"slots": {
				"origin": {
					"name": "origin",
					"value": "coolmine",
					"resolutions": {
						"resolutionsPerAuthority": [
							{
								"authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.5c6dcd7c-95cb-44fe-9d69-733d97006734.Train_Origins",
								"status": {
									"code": "ER_SUCCESS_MATCH"
								},
								"values": [
									{
										"value": {
											"name": "coolmine",
											"id": "72c35c85d5d93bd935d4baf3a24934b5"
										}
									}
								]
							}
						]
					},
					"confirmationStatus": "NONE",
					"source": "USER"
				},
				"direction": {
					"name": "direction",
					"value": "maynooth",
					"resolutions": {
						"resolutionsPerAuthority": [
							{
								"authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.5c6dcd7c-95cb-44fe-9d69-733d97006734.AMAZON.AT_REGION",
								"status": {
									"code": "ER_SUCCESS_MATCH"
								},
								"values": [
									{
										"value": {
											"name": "maynooth",
											"id": "551fa7014c090502de84dd7d4fe32ec6"
										}
									}
								]
							}
						]
					},
					"confirmationStatus": "NONE",
					"source": "USER"
				}
			}
		},
		"dialogState": "COMPLETED"
	}
}
'''