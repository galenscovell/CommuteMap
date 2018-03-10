"""
Defines a Location containing name, central point, and region boundaries via NW and SW point.

@author GalenS <galen.scovell@gmail.com>
"""

from models.point import Point


class Location(dict):
    def __init__(self, details):
        super(Location, self).__init__()

        self['address'] = details['formatted_address']

        geometry = details['geometry']
        self['center'] = Point(geometry['location']['lat'], geometry['location']['lng'])

        bounds = geometry['bounds']
        self['northeast'] = Point(bounds['northeast']['lat'], bounds['northeast']['lng'])
        self['southwest'] = Point(bounds['southwest']['lat'], bounds['southwest']['lng'])
