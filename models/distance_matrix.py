"""
Defines a Distance containing search terms and travel distance/time.

@author GalenS <galen.scovell@gmail.com>
"""


class DistanceMatrix(dict):
    def __init__(self, origin, destination, row):
        super(DistanceMatrix, self).__init__()

        self['start'] = origin
        self['end'] = destination

        elements = row['elements'][0]
        self['distance'] = elements['distance']['text']
        self['duration'] = int(elements['duration']['value'])
