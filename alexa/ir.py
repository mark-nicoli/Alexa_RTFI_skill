from xml.dom import minidom
import datetime,logging,requests

STATION_TYPE = {
    'mainline': 'M',
    'suburban': 'S',
    'dart': 'D'
}

_LOGGER = logging.getLogger(__name__)

#get a value from a tag (if it exists)
def tag(station, tag_name):
    tag = station.getElementsByTagName(tag_name)[0].firstChild
    if tag:
        return tag.nodeValue

    return None

#parse xml data into a python map
def parse(data, obj_name, a_map):
    parsedXML = minidom.parseString(data)
    parsedObjects = []
    for obj in parsedXML.getElementsByTagName(obj_name):
        parsed_obj = {}
        for (py_name, xml_name) in a_map.items():
            parsed_obj[py_name] = tag(obj, xml_name)
        parsedObjects.append(parsed_obj)
    return parsedObjects

#rail api interactions
class IrishRailRTPI(object):
    def parse_stations(self, data):
        #parse the station list
        a_map = {
            'name': 'StationDesc',
            'alias': 'StationAlias',
            'lat': 'StationLatitude',
            'long': 'StationLongitude',
            'code': 'StationCode',
            'id': 'StationId',
        }
        return parse(data, 'objStation', a_map)

    def stations(self, data):
        #parse the station data
        a_map = {
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
        return parse(data, 'objStationData', a_map)

    def trains(self, url):
        #parse train data
        a_map = {
            'status': 'TrainStatus',
            'latitude': 'TrainLatitude',
            'longitude': 'TrainLongitude',
            'code': 'TrainCode',
            'date': 'TrainDate',
            'message': 'PublicMessage',
            'direction': 'Direction'
        }
        return parse(url, 'objTrainPositions', a_map)

    def movement(self, url):
        #parse train data
        a_map = {
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
        return parse(url, 'objTrainMovements', a_map)

    def get_station(self,station_name,num_minutes=None,direction=None,destination=None,stops_at=None):
        url = self.api_base_url + 'getStationDataByNameXML'
        params = {
            'StationDesc': station_name
        }
        if num_minutes:
            url = url + '_withNumMins'
            params['NumMins'] = num_minutes
        resp = requests.get(url, params=params, timeout=10)
        
        if resp.status_code != 200:
            return []
        trains = self.stations(resp.content)

        if direction is not None or destination is not None:
            return self.pruned_trains(trains,direction=direction,destination=destination,stops_at=stops_at)
        return trains

    def get_train_stops(self, train_code, date=None):
        if date is None:
            date = datetime.date.today().strftime("%d %B %Y") #todays date
        url = self.api_base_url + 'getTrainMovementsXML'
        params = {
            'TrainId': train_code,
            'TrainDate': date
        }
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return []
        return self.movement(resp.content)

    def __init__(self):
        self.api_base_url = 'http://api.irishrail.ie/realtime/realtime.asmx/'
