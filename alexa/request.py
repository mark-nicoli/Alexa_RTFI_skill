import db
import json
from ir import IrishRailRTPI
import string
#Get time for next bus
#mark = 'smart' if haim == 'old' else 'dumb'

def dbus_times():
    route = input('Enter route number: ')
    form_route = route.translate({ord(c): None for c in string.whitespace})
    print(form_route)
    stop_number = input('Enter stop number: ')   #4825
    g = db.RtpiApi(user_agent='test')
    bus_times = g.rtpi(stop_number, form_route)
    next_bus = bus_times.results[0]['duetime']

    try:
        if next_bus == "Due":
            print( "the next {} bus calling at stop {} is due now ".format(form_route,str(stop_number)))
        else:
            print("the next {} bus calling at stop: {} is in {} minutes".format(form_route, str(stop_number),str(next_bus)))

    except:
        print("there are currently no such buses at the requested stop")
# get time for next train
def rail_time():
    train_times = IrishRailRTPI()
    
    # input type{
    #     pearse station: Dublin pearse
    #     connolly: Dublin Connolly
    # }
    
    origin = input('origin: ')
    destination = input('destination: ').lower()
    '''
        get all the trains calling at a station:origin
        def get_station_by_name(self,station_name,num_minutes=None,direction=None,destination=None,stops_at=None):
    '''
    data = json.dumps(train_times.get_station_by_name(origin, destination, stops_at = destination), indent=4, sort_keys=True)
    resp = json.loads(data) #we get a list of dictionaries
    # print(len(resp))
    #print(resp)
    for i in range(0,len(resp)):
        dict_data = resp[i]
        oi = dict_data['destination']
        if oi.lower()==destination: #filter out by origin and make into lower case for alexa
            '''
                origin = coolmine.
                expected_arrival_time = time train arrives at coolmine
                due_in_mins = mins to arrival of train
            '''
            dict_data2 = resp[i+1]
            if dict_data['due_in_mins'] == 'Due': #avoid 'next train is due in due minutes' output
                return ('Your train is due now')
            elif int(dict_data['due_in_mins']) <= 20:
                return ('The next trains are in {} and {} mins'.format(dict_data['due_in_mins'], dict_data2['due_in_mins']))
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
