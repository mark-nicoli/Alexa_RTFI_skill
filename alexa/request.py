import db
import json
from ir import IrishRailRTPI
import string

def dbus_times():
    route = input('Enter route number: ')
    form_route = route.translate({ord(c): None for c in string.whitespace})
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
    data = json.dumps(train_times.get_station(origin, destination), indent=4, sort_keys=True)
    resp = json.loads(data) #we get a list of dictionaries

    for i in range(len(resp)):
        if resp[i]['destination'].lower()==destination: #filter out by origin and make into lower case for alexa
            if resp[i]['due_in_mins'] == 'Due': #avoid 'next train is due in due minutes' output
                return ('Your train is due now')
            else:
                return ('The next train is in {} mins'.format(resp[i]['due_in_mins']))
            break

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

