#!/usr/bin/env python
from datetime import datetime
from datetime import timezone
from finder import GoogleMap
from weather import commuteWeather

import os
import pytz
import json


gmap=GoogleMap()
weather=commuteWeather()
weather_locs=dict()


def partofday(hr):
    if hr < 6 :
        return 'early_morning'
    elif 6 <= hr < 12:
        return 'morning'
    elif 12 <= hr < 16:
        return 'afternoon'
    elif 16 <= hr < 20:
        return 'evening'
    elif 20 <= hr < 23:
        return 'night'

def saveCommute():

    tz=pytz.timezone('Asia/Kolkata')
    dt=datetime.now(tz)
    weekday=dt.weekday()
    daypart=partofday(dt.hour)

    # arrival time of the transit at origin
    arrival_time=int(dt.replace(tzinfo=timezone.utc).timestamp())
    arrival_time+=300 # 5 min in future

    # get first 10 addresses from the addressess.json and keep them as
    # origins and destinations
    with open('data/addresses.json', 'r') as f:
        addr=json.load(f)

    origins = [origin + ' bus stop, bangalore, India' 
            for origin in addr['addresses'][0:10]]
    destinations = [destination + ' bus stop, bangalore, India' 
            for destination in addr['addresses'][0:10]]

    units='metric'
    mode='transit'
    transit_mode='bus'


    matrix_result=gmap.distance_matrix(
            arrival_time=arrival_time,
            origins=origins,
            destinations=destinations,
            mode=mode,
            transit_mode=transit_mode,
            units=units)

    # import pdb;pdb.set_trace()
    #TODO: flatten the matrix
    with open(f'commutes_{arrival_time}.csv', 'w') as f:
        ix=0
        for i in matrix_result['origin_addresses']:
            iy=0
            for j in matrix_result['destination_addresses']:
                row_elements = matrix_result['rows'][ix]['elements'][iy]

                if row_elements['status'] == 'OK':
                    dist_text=row_elements['distance']['text']
                    dist_value=row_elements['distance']['value']
                    dur_text=row_elements['duration']['text']
                    dur_value=row_elements['duration']['value']

                    line=cleanresultrow(i, j, dist_text, dist_value, dur_text, dur_value)
                    orig_dest_id=f'{getGeoId(i)[0]}, {getGeoId(i)[1]}, {getGeoId(j)[0]}, {getGeoId(j)[1]}'

                    # get the route weather details
                    weather_details=getrouteWeatherDetails(orig_dest_id)

                    line=f'{orig_dest_id},{weekday},{daypart},{line},{weather_details}'
                    #print(line)
                    f.write(line+"\n")

                iy+=1
            ix+=1

def getrouteWeatherDetails(orig_dest_id):
    """ Method to get current weather details using coordinates"""

    orig_dest_id_list=orig_dest_id.split(",")
    origin=(orig_dest_id_list[0].strip(), 
            orig_dest_id_list[1].strip())
    destination=(orig_dest_id_list[2].strip(), 
            orig_dest_id_list[3].strip())

    # do not send api request if weather is aleardy stored for a location
    if origin not in weather_locs:
        origin_weather=weather.get_yahoo_weather_by_location(*origin)
        weather_locs.update({origin:origin_weather})
    else:
        origin_weather=weather_locs[origin]

    if destination not in weather_locs:
        destination_weather=weather.get_yahoo_weather_by_location(*destination)
        weather_locs.update({destination: destination_weather})
    else:
        destination_weather=weather_locs[destination]

    origin_condtns=origin_weather.current_observation.condition.as_dict().values()
    origin_wind=origin_weather.current_observation.wind.as_dict().values()
    origin_atmos=origin_weather.current_observation.atmosphere.as_dict().values()

    destination_condtns=destination_weather.current_observation.condition.as_dict().values()
    destination_wind=destination_weather.current_observation.wind.as_dict().values()
    destination_atmos=destination_weather.current_observation.atmosphere.as_dict().values()

    row=','.join([str(x) for x in list(origin_condtns)])+","
    row+=','.join([str(x) for x in list(origin_wind)])+","
    row+=','.join([str(x) for x in list(origin_atmos)])+","
    row+=','.join([str(x) for x in list(destination_condtns)])+","
    row+=','.join([str(x) for x in list(destination_wind)])+","
    row+=','.join([str(x) for x in list(destination_atmos)])

    return row

def getGeoId(location):
    result=gmap.geocode(location)
    lat=result[0]['geometry']['location']['lat']
    lng=result[0]['geometry']['location']['lng']
    geoId=f'{lat}__{lng}'
    return [lat, lng]

def cleanresultrow(i, j, dist_text, dist_value, dur_text, dur_value):
    i=i.replace(","," ")
    j=j.replace(","," ")
    #dist_text=dist_text.replace(",", " ")
    #dist_value=dist_value.replace(",", " ")
    #dur_text=dur_text.replace(",", " ")
    #dur_value=dur_value.replace(",", " ")
    return ','.join([i, j, str(dist_text), str(dist_value), str(dur_text), str(dur_value)])

if __name__=="__main__":
    saveCommute()
