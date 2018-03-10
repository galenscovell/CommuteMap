"""
Entrypoint for commute map tool.

Fill in `params.json` with desired values, then run `python run.py`

@Author GalenS <galen.scovell@gmail.com>
"""

import json

from datetime import datetime

import util.constants as constants

from graphics.visualizer import Visualizer
from services.google_maps_client import MapClient


def extract_params():
    with open(constants.params_path, 'rb') as f:
        contents = f.read().strip()
    p = json.loads(contents)
    p['arrival_time'] = datetime.strptime(p['arrival_time'], '%m/%d/%y %H:%M')

    return p


def fill_locations(location_list, client):
    locations = []
    for l in location_list:
        locations.append(client.find_location_details(l))

    return locations


def create_google_maps_client():
    client = None
    try:
        client = MapClient()
    except Exception as ex:
        print('Unable to generate map client - {0}'.format(ex))
        client = None
    finally:
        return client


if __name__ == '__main__':
    params = extract_params()
    print('Arrive by: {0}'.format(params['arrival_time']))

    map_client = create_google_maps_client()

    # Fill in origins and destinations as detailed Locations
    origins = fill_locations(params['origins'], map_client)
    destinations = fill_locations(params['destinations'], map_client)

    # Calculate distance matrix between origins and destinations
    distance_matrix = map_client.get_distance_matrix(origins, destinations, params['arrival_time'])

    mapper = Visualizer(origins, destinations, distance_matrix)
