#
# Author:       cayscays
# Date:         November 2021
# Version:      1
#

import random

# Constants:
GRID_HEIGHT = 12
GRID_WIDTH = 25

MAX_WIND = 63  # in Knot
MAX_TEMP = 50  # in Celsius
MIN_TEMP = -30  # in Celsius
WIND_DIRECTIONS = ['<', 'v', '>', '^']
LAYOUT_OPTIONS = ['Sea', 'Ice', 'Land', 'City', 'Forest']
MAX_HEIGHT = 700
MIN_HEIGHT = -300

PARAMS = ['wind', 'temperature', 'pollution', 'clouds', 'rain', 'height', 'landscape']


# Helper functions:

# --> Random boolean value
def random_bool():
    return random.choice([True, False])
