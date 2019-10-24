from xml.dom import minidom
import datetime
import logging
import requests


STATION_TYPE_TO_CODE_DICT = {
    'mainline': 'M',
    'suburban': 'S',
    'dart': 'D'
}

_LOGGER = logging.getLogger(__name__)


def _get_minidom_tag_value(station, tag_name):
    """get a value from a tag (if it exists)"""
    tag = station.getElementsByTagName(tag_name)[0].firstChild
    if tag:
        return tag.nodeValue

    return None

def _parse(data, obj_name, attr_map):
    """parse xml data into a python map"""
    parsed_xml = minidom.parseString(data)
    parsed_objects = []
    for obj in parsed_xml.getElementsByTagName(obj_name):
        parsed_obj = {}
        for (py_name, xml_name) in attr_map.items():
            parsed_obj[py_name] = _get_minidom_tag_value(obj, xml_name)
        parsed_objects.append(parsed_obj)
    return parsed_objects


class IrishRailRTPI(object):
    #interactions with irish railAPI
    def _parse_station_list(self, data):
        """parse the station list"""
        attr_map = {
            'name': 'StationDesc',
            'alias': 'StationAlias',
            'lat': 'StationLatitude',
            'long': 'StationLongitude',
            'code': 'StationCode',
            'id': 'StationId',
        }
        return _parse(data, 'objStation', attr_map)

    def _parse_station_data(self, data):
        """parse the station data"""
        attr_map = {
            'code': 'Traincode',
            'origin': 'Origin',
            'destination': 'Destination',
            'origin_time': 'Origintime',
            'destination_time': 'Destinationtime',
            'due_in_mins': 'Duein',
            'late_mins': 'Late',
            'expected_arrival_time': 'Exparrival',
            'expected_departure_time': 'Expdepart',
            'scheduled_arrival_time': 'Scharrival',
            'scheduled_departure_time': 'Schdepart',
            'type': 'Traintype',
            'direction': 'Direction',
            'location_type': 'Locationtype',
        }
        return _parse(data, 'objStationData', attr_map)

    def _parse_all_train_data(self, url):
        """parse train data"""
        attr_map = {
            'status': 'TrainStatus',
            'latitude': 'TrainLatitude',
            'longitude': 'TrainLongitude',
            'code': 'TrainCode',
            'date': 'TrainDate',
            'message': 'PublicMessage',
            'direction': 'Direction'
        }
        return _parse(url, 'objTrainPositions', attr_map)

    def _parse_train_movement_data(self, url):
        """parse train data"""
        attr_map = {
            'code': 'TrainCode',
            'date': 'TrainDate',
            'location_code': 'LocationCode',
            'location': 'LocationFullName',
            'origin': 'TrainOrigin',
            'destination': 'TrainDestination',
            'expected_arrival_time': 'ExpectedArrival',
            'expected_departure_time': 'ExpectedDeparture',
            'scheduled_arrival_time': 'ScheduledArrival',
            'scheduled_departure_time': 'ScheduledDeparture',
        }
        return _parse(url, 'objTrainMovements', attr_map)

    def get_station_by_name(self,station_name,num_minutes=None,direction=None,
                            destination=None,
                            stops_at=None):
        url = self.api_base_url + 'getStationDataByNameXML'
        params = {
            'StationDesc': station_name
        }
        if num_minutes:
            url = url + '_withNumMins'
            params['NumMins'] = num_minutes
        response = requests.get(
            url, params=params, timeout=10)
        if response.status_code != 200:
            return []
        trains = self._parse_station_data(response.content)
        if direction is not None or destination is not None:
            return self._prune_trains(trains,
                                      direction=direction,
                                      destination=destination,
                                      stops_at=stops_at)
        return trains

    def _prune_trains(self, trains, direction=None,
                      destination=None, stops_at=None):
        pruned_data = []
        for train in trains:
            append = True
            if direction is not None and train["direction"] != direction:
                append = False

            if destination is not None and train["destination"] != destination:
                append = False

            if append and stops_at is not None:
                if stops_at != train['destination']:
                    stops = self.get_train_stops(train["code"])
                    for stop in stops:
                        append = False
                        if stop["location"] == stops_at:
                            append = True
                            break
            if append:
                pruned_data.append(train)
        return pruned_data

    def get_train_stops(self, train_code, date=None):
        """Get details for a train.
        @param train_code code for the trian
        @param date Date in format "15 oct 2017". If none use today
        """
        if date is None:
            date = datetime.date.today().strftime("%d %B %Y")
        url = self.api_base_url + 'getTrainMovementsXML'
        params = {
            'TrainId': train_code,
            'TrainDate': date
        }
        response = requests.get(
            url, params=params, timeout=10)
        if response.status_code != 200:
            return []
        return self._parse_train_movement_data(response.content)

    def __init__(self):
        self.api_base_url = 'http://api.irishrail.ie/realtime/realtime.asmx/'
