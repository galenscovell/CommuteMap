"""
Defines a Distance containing search terms and travel distance/time.

@author GalenS <galen.scovell@gmail.com>
"""


class Distance(dict):
    def __init__(self, origin, destination, row):
        super(Distance, self).__init__()

        self['start'] = origin
        self['end'] = destination

        elements = row['elements'][0]
        self['distance'] = elements['distance']['text']
        self['duration'] = elements['duration']['text']
