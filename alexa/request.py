import db
import json
from ir import IrishRailRTPI
#Get time for next bus
#mark = 'smart' if haim == 'old' else 'dumb'

def dbus_times():
    route = input('Enter route number: ')
    stop_number = input('Enter stop number: ')   #4825
    g = db.RtpiApi(user_agent='test')
    bus_times = g.rtpi(stop_number, route)
    print (bus_times)
    #print(my_stop.timestamp)
    if bus_times.results[0]['duetime'] != 'due':
        return ('the next {} bus is in {} mins'.format(route, bus_times.results[0]['duetime']))
    else:
        return ('bus is due now')
# get time for next train
def rail_time():
    train_times = IrishRailRTPI()
    
    # input type{
    #     pearse station: Dublin pearse
    #     connolly: Dublin Connolly
    # }
    
    origin = input('origin: ')
    destination = input('destination: ').lower()
    stops = 'castleknock'.lower()
    # #dir = input('direction: ')
    # num_mins = 30
    '''
        get all the trains calling at a station:origin
        def get_station_by_name(self,station_name,num_minutes=None,direction=None,destination=None,stops_at=None):
    '''
    data = json.dumps(train_times.get_station_by_name(origin, destination, stops_at = destination), indent=4, sort_keys=True)
    resp = json.loads(data)

    for i in range(len(resp)):
        dict_data = resp[i]
        if dict_data['destination'].lower()==destination: #filter out by origin and make into lower case for alexa
            print(dict_data['destination'].lower())  # visualization of json data
            print(destinations)
            '''
                origin = coolmine.
                expected_arrival_time = time train arrives at coolmine
                due_in_mins = mins to arrival of train
            '''
            if dict_data['due_in_mins'] == 'Due': #avoid 'next train is due in due minutes' output
                return ('Your train is due now')
            else:
                return ('The next train is in {} mins'.format(dict_data['due_in_mins']))

def main():
    serv = input("train or bus times: ")
    if serv=='bus':
        print (dbus_times())
    elif serv=='train':
        print (rail_time())
    else:
        print('rahhh... you stupid')

if __name__ == '__main__':
    main()

#4825 - test bus stop
