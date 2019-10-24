import db
import json
from ir import IrishRailRTPI
#Get time for next bus
#mark = 'smart' if haim == 'old' else 'dumb'

def dbus_times():
    route = input('Enter route number: ')
    stop_number = input('Enter stop number: ')
    g = db.RtpiApi(user_agent='test')
    bus_times = g.rtpi(stop_number, route)
    #print(my_stop.timestamp)
    return ('the next {} bus is in in {} mins'.format(route, bus_times.results[0]['duetime']))
# get time for next train
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
            #print(dict_data)
            return ('the next {} train is in {} mins'.format(dir, dict_data['due_in_mins']))

        '''print(dict_data)
        print('The next {} train is in {} minutes'.format(dir, dict_data['due_in_mins']))'''

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
