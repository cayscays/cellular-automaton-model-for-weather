#
# Author:       cayscays
# Date:         November 2021
# Version:      1
# Class cell: handles cell's initiation and operations
#

import model.rules as rules
from model.helper import *

WEATHER_SYMBOLS_AS_STRINGS = {'clouds': '☁',
                              'no clouds': '☀',
                              'rain': '☂',
                              'snow': '❆',
                              'pollution': '▓▓▓▓▓▓▓▓\n▓▓▓▓▓▓▓▓\n▓▓▓▓▓▓▓▓'}


# A complete random cell
# def cell_from_random_no_init_rules():
#     return Cell(wind_speed=random.randint(0, MAX_WIND), wind_direction=random.choice(WIND_DIRECTIONS),
#                 temp=random.randint(MIN_TEMP, MAX_TEMP), pollution=randomBool(), clouds=randomBool(),
#                 height=random.randint(MIN_HEIGHT, MAX_HEIGHT), landscape=random.choice(LAYOUT_OPTIONS),
#                 rain=randomBool())

# Landscape --> Cell following init rules
def cell_from_landscape_with_init_rules(landscape):
    return Cell(wind_speed=rules.wind_speed_init(),
                wind_direction=rules.wind_direction_init(),
                temp=rules.temp_init(landscape),
                pollution=rules.pollution_init(),
                clouds=rules.clouds_init(),
                height=rules.height_init(landscape),
                landscape=landscape,
                rain=rules.rain_init())


# Random Cell following init rules
def cell_from_random_with_init_rules():
    return cell_from_landscape_with_init_rules(random.choice(LAYOUT_OPTIONS))


class Cell:
    def __init__(self, wind_speed, wind_direction, temp, pollution, clouds, height, landscape, rain):
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.temp = temp
        self.pollution = pollution
        self.clouds = clouds
        self.height = height
        self.landscape = landscape
        self.rain = rain

    # Deep copy
    def deep_copy(self):
        return Cell(wind_speed=self.wind_speed,
                    wind_direction=self.wind_direction,
                    temp=self.temp,
                    pollution=self.pollution,
                    clouds=self.clouds,
                    height=self.height,
                    landscape=self.landscape,
                    rain=self.rain)

    # Parameter --> Formatted text to display on the gui
    def get_text(self, param):
        text = ""
        color = 'black'
        font_size = 11
        if param == 'wind':
            if self.wind_speed == 0:
                wind_direction = ""
            else:
                wind_direction = self.wind_direction
            text = str(self.wind_speed) + " " + wind_direction
        elif param == 'temperature':
            text = str(self.temp) + "°C"
        elif param == 'pollution':
            if self.pollution:
                text = WEATHER_SYMBOLS_AS_STRINGS['pollution']
                color = 'black'
        elif param == 'clouds':
            font_size = 20
            if self.clouds:
                text = WEATHER_SYMBOLS_AS_STRINGS['clouds']
                color = 'white'
            else:
                text = WEATHER_SYMBOLS_AS_STRINGS['no clouds']
                color = 'yellow'
        elif param == 'rain':
            font_size = 27
            if self.rain:
                if self.temp >= 0:
                    text = WEATHER_SYMBOLS_AS_STRINGS['rain']
                    color = 'maroon'
                else:
                    text = WEATHER_SYMBOLS_AS_STRINGS['snow']
                    color = 'aliceblue'
        elif param == 'height':
            text = str(self.height) + "m"
        elif param == 'landscape':
            text = self.landscape
        return text, color, font_size

    def get_state(self):
        return [self.landscape, self.wind_direction, self.wind_speed, self.temp, self.pollution, self.clouds,
                self.height, self.rain]

    # Update the cell to its state on the next generation
    def update(self, nw, n, ne,
               w, e,
               se, s, sw):
        previous_state = self.deep_copy()

        next_wind = rules.update_wind(previous_state.wind_direction,
                                      [n.wind_speed, w.wind_speed, e.wind_speed, s.wind_speed],
                                      [n.wind_direction, w.wind_direction, e.wind_direction, s.wind_direction])
        self.wind_speed = next_wind[0]
        self.wind_direction = next_wind[1]
        self.pollution = rules.update_pollution(previous_state.landscape, previous_state.rain,
                                                n.pollution, w.pollution, e.pollution, s.pollution,
                                                n.wind_direction, w.wind_direction, e.wind_direction, s.wind_direction)

        self.temp = rules.update_temp(landscape=previous_state.landscape, clouds=previous_state.clouds,
                                      pollution=previous_state.pollution, prev_temp=previous_state.temp,
                                      temps=[n.temp, w.temp, e.temp, s.temp])
        self.clouds = rules.update_clouds(previous_state.rain, previous_state.clouds, previous_state.wind_speed,
                                          previous_state.landscape, n.clouds, s.clouds, e.clouds, w.clouds,
                                          n.wind_direction, s.wind_direction, e.wind_direction, w.wind_direction)
        landscape_and_height = rules.landscape_and_height_update(previous_state.landscape, previous_state.height,
                                                                 previous_state.temp,
                                                                 [nw.landscape, n.landscape, ne.landscape, w.landscape,
                                                                  e.landscape, se.landscape, s.landscape, sw.landscape],
                                                                 [nw.height, n.height, ne.height, w.height, e.height,
                                                                  se.height, s.height, sw.height])
        self.landscape = landscape_and_height[0]
        self.height = landscape_and_height[1]
        self.rain = rules.update_rain(previous_state.clouds, nw.clouds, n.clouds, ne.clouds,
                                      w.clouds, e.clouds,
                                      se.clouds, s.clouds, sw.clouds)
