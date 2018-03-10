"""
Values used throughout tool.

@author GalenS <galen.scovell@gmail.com>
"""

import os

params_path = os.path.join(os.getcwd(), 'params.json')

# Dimensions
window_x = 640
window_y = 960
cell_size = 5
margin = 1

# Color setup
c_background = (62, 70, 73)
c_empty = (47, 47, 49)
c_origin = (34, 168, 109)
c_destination = (233, 110, 68)

# Misc
frame_rate = 60
empty_id = 0
origin_id = 1
destination_id = 2
