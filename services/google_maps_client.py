"""
Client for interacting with the Google Maps API.

@Author GalenS <galen.scovell@gmail.com>
"""

import googlemaps

from models.distance_matrix import DistanceMatrix
from models.location import Location


class MapClient:
    def __init__(self):
        self.client = googlemaps.Client(key='AIzaSyAoo39xmVMOA6K90WzGNF_se9eKpuw0VG8')

    def find_location_details(self, search_term):
        location = None
        try:
            result = self.client.geocode(search_term)
            location = Location(result[0])
        except Exception as ex:
            print('Unable to get location details - {0}'.format(ex))
            location = None
        finally:
            return location

    def get_distance_matrix(self, start, end, arrival_time):
        details = self.client.distance_matrix(
            origins=[s['address'] for s in start if 'address' in s],
            destinations=[e['address'] for e in end if 'address' in e],
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
            # Multiple-to-destination
            for x in range(0, len(origins)):
                distances.append(DistanceMatrix(origins[x], destinations[0], result_rows[x]))
        elif len(destinations) > 1:
            # Multiple-from-origin
            for x in range(0, len(destinations)):
                distances.append(DistanceMatrix(origins[0], destinations[x], result_rows[x]))
        else:
            # Single origin to single destination
            distances.append(DistanceMatrix(origins[0], destinations[0], result_rows[0]))

        return distances
