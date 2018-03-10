"""
Defines a Location containing name, central point, and region boundaries via NW and SW point.

@author GalenS <galen.scovell@gmail.com>
"""

import math


class Location(dict):
    def __init__(self, details):
        super(Location, self).__init__()

        if 'address' in details:
            self['label'] = details['address']
            self['address'] = details['address']
        else:
            self['label'] = details['address_components'][0]['long_name']
            self['address'] = details['formatted_address']

        if 'geometry' in details:
            geometry = details['geometry']
            bounds = geometry['bounds']
            self['center'] = [geometry['location']['lat'], geometry['location']['lng']]
            self['northeast'] = [bounds['northeast']['lat'], bounds['northeast']['lng']]
            self['southwest'] = [bounds['southwest']['lat'], bounds['southwest']['lng']]
        else:
            self['center'] = [details['center'][0], details['center'][1]]
            self['northeast'] = [details['northeast'][0], details['northeast'][1]]
            self['southwest'] = [details['southwest'][0], details['southwest'][1]]

        self['width'] = math.fabs(self['northeast'][0] - self['southwest'][0])
        self['height'] = math.fabs(self['northeast'][1] - self['southwest'][1])
