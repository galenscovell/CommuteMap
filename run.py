"""


@Author GalenS <galen.scovell@gmail.com>
"""

import googlemaps
import json

from datetime import datetime

import util.constants as constants

from models.distance import Distance
from models.location import Location


distance_api_key = 'AIzaSyAoo39xmVMOA6K90WzGNF_se9eKpuw0VG8'


def extract_params():
    with open(constants.params_path, 'rb') as f:
        contents = f.read().strip()
    p = json.loads(contents)
    p['arrival_time'] = datetime.strptime(p['arrival_time'], '%m/%d/%y %H:%M')

    return p


def create_google_maps_client():
    return googlemaps.Client(key=distance_api_key)


def get_location_details(client, location_string):
    details = client.geocode(location_string)
    return Location(details[0])


def get_transit_time_between_points(client, start, end, arrival_time):
    details = client.distance_matrix(
        origins=[s['address'] for s in start],
        destinations=[e['address'] for e in end],
        mode='transit',
        units='imperial',
        arrival_time=arrival_time,
        traffic_model='best_guess',
        transit_routing_preference='fewer_transfers'
    )

    origins = details['origin_addresses']
    destinations = details['destination_addresses']
    result_rows = details['rows']

    distances = []
    if len(origins) > 1:
        # Multiple origins
        for x in range(0, len(origins)):
            distances.append(Distance(origins[x], destinations[0], result_rows[x]))
    else:
        # Multiple destinations
        for x in range(0, len(destinations)):
            distances.append(Distance(origins[0], destinations[x], result_rows[x]))

    return distances


if __name__ == '__main__':
    params = extract_params()
    map_client = create_google_maps_client()

    start_locations = []
    for l in params['start']:
        start_locations.append(get_location_details(map_client, l))

    end_locations = []
    for l in params['end']:
        end_locations.append(get_location_details(map_client, l))

    print(start_locations)
    print(end_locations)
    print(params['arrival_time'])

    print(get_transit_time_between_points(map_client, start_locations, end_locations, params['arrival_time']))

    # TODO: Associate distance START and END values with initial Locations to get coordinates and boundaries
    # Throw these into a chart somehow
