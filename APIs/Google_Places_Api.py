'''

Downloaded from: https://github.com/googlemaps/google-maps-services-python/tree/master/googlemaps
-- USE THE FOLLOWING COMMAND pip install googlemaps
'''

import googlemaps
from datetime import datetime
from . import config

APIKEY = config.api_key_google_places

def get_coords(loc):
    gmaps = googlemaps.Client(key=APIKEY)
    geocode_result = gmaps.geocode(loc)
    lat, lng = geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
    return lat, lng


def get_restaurants_near_place(location,typeofplace):
    gmaps = googlemaps.Client(key=APIKEY)

    # Geocoding an address
    # geocode_result = gmaps.geocode(location)

    # Look up an address with reverse geocoding
    #reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

    # lat,lng = geocode_result[0]['geometry']['location']['lat'],geocode_result[0]['geometry']['location']['lng']

    lat, lng = get_coords(location)
    # Request directions via public transit
    result = gmaps.places(typeofplace,location=[lat,lng],radius=2000)

    return result

def get_museums(loc):
    gmaps = googlemaps.Client(key=APIKEY)
    lat, lng = get_coords(loc)
    result = gmaps.places("Museums", location=[lat, lng], radius=2000)
    return result