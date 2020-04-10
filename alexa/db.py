#!/usr/bin/python3
from sys import exit
import requests

class RtpiApi(): #interaction with API
    RTPI_SERV = 'https://data.smartdublin.ie/cgi-bin/rtpi/'

    def __init__(self, user_agent=None):
        self.user_agent = {'User-Agent': user_agent}

    def rtpi(self, stop, route=None, max_results=None, operator=None):
        #real time passenger info wrapper
        args = {'stopid': stop}

        if route:
            args['routeid'] = route
        if max_results:
            args['maxresults'] = max_results
        if operator:
            args['operator'] = operator

        return self._make_request('realtimebusinformation', args)
        #return self._make_request('realtimetraininformation', args)

    def stop_info(self, stop=None, stop_name=None, operator=None):
    #   stop information wrapper
        args = {}
        if stop:
            args['stopid'] = stop
        if stop_name:
            args['stopname'] = stop_name
        if operator:
            args['operator'] = operator

        return self._make_request('busstopinformation', args)

    def route_info(self, route, operator):
    #   route information wrapper
        args = {'routeid': route, 'operator': operator}

        return self._make_request('routeinformation', args)

    def _make_request(self, uri_extens, req_items):
    #   build request object and pass container back
        resp = requests.get(self.RTPI_SERV + uri_extens, params=req_items,headers=self.user_agent)
        resp_json = resp.json()
        return Data(resp_json)


class Data:
    '''A container class returned to user for cleaner data access.'''
    def __init__(self, response):
        for key, value in response.items():
            setattr(self, key, value)
