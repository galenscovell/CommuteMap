"""
Defines a Location containing name, central point, and region boundaries via NW and SW point.

@author GalenS <galen.scovell@gmail.com>
"""

import math


class Location(dict):
    def __init__(self, details):
        super(Location, self).__init__()

        if 'address' in details:
            self['address'] = details['address']
        else:
            self['address'] = details['formatted_address']

        if 'geometry' in details:
            geometry = details['geometry']
            bounds = geometry['bounds']
            self['center'] = [geometry['location']['lat'], geometry['location']['lng']]
            self['up_right'] = [bounds['northeast']['lat'], bounds['northeast']['lng']]
            self['down_left'] = [bounds['southwest']['lat'], bounds['southwest']['lng']]
        else:
            self['center'] = [details['center'][0], details['center'][1]]
            self['up_right'] = [details['northeast'][0], details['northeast'][1]]
            self['down_left'] = [details['southwest'][0], details['southwest'][1]]

        # Calculate rest of bounding box from up_right and down_left points
        self['up_left'] = [self['down_left'][0], self['up_right'][1]]
        self['down_right'] = [self['up_right'][0], self['down_left'][1]]

        self['width'] = math.fabs(self['down_right'][0] - self['down_left'][0])
        self['height'] = math.fabs(self['down_right'][1] - self['up_right'][1])
