"""
Defines a Point containing geospatial coordinates.

@author GalenS <galen.scovell@gmail.com>
"""


class Point(list):
    def __init__(self, latitude, longitude):
        self.append(latitude)
        self.append(longitude)
