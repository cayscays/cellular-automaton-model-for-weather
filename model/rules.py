#
# Author:       cayscays
# Date:         November 2021
# Version:      1
# The cellular automaton rules
# 

from model.cell import *


# initiation rules:
# ===========================================

def wind_speed_init():
    return random.randint(0, MAX_WIND)


def pollution_init():
    return False


def clouds_init():
    return False


# Sea levels all begin at 0. other landscapes are higher.
def height_init(landscape):
    height = 0  # if landscape == 'sea'
    if landscape != 'Sea':
        height = random.randint(0, MAX_HEIGHT)
    return height


def rain_init():
    return False


def wind_direction_init():
    return random.choice(WIND_DIRECTIONS)


# Ice is -30 to -20 degrees Celsius 
# Sea is 10 to 30  
# Others are -10 to 35
def temp_init(landscape):
    temp = random.randint(-10, 35)
    if landscape == 'Ice':
        temp = random.randint(MIN_TEMP, -20)
    elif landscape == 'Sea':
        temp = random.randint(10, 30)
    return temp


# generations rules
# ===========================================

# Rains if cell has clouds + 2 neighbors at least has clouds.
def update_rain(prev_clouds, clouds0, clouds1, clouds2, clouds3, clouds4, clouds5, clouds6, clouds7):
    if prev_clouds is True:
        number_of_cells_with_clouds = 0
        environment_cloud_states = [prev_clouds, clouds0, clouds1, clouds2, clouds3, clouds4, clouds5, clouds6,
                                    clouds7]
        # count how many clouds are in the cell's environment
        for cell in environment_cloud_states:
            if cell:
                number_of_cells_with_clouds += 1
        return number_of_cells_with_clouds >= 3
    else:
        return False


# The next wind speed is (the highest neighboring wind speed * 2) % MAX_WIND
def update_wind(prev_wind_direction, wind_speeds, wind_directions):
    wind_speed = 0
    wind_direction = prev_wind_direction
    for i in range(len(wind_speeds)):
        if wind_speeds[i] > wind_speed:
            wind_speed = wind_speeds[i]
            wind_direction = wind_directions[i]
    wind_speed = int((wind_speed * 2) % MAX_WIND)
    return min(MAX_WIND, int(wind_speed)), wind_direction


# Updates pollution according to pollution counter, if the counter > 0 returns polluted cell, otherwise: clean.
# Rain and forests decrease the counter and city and incoming pollution increases it.
def update_pollution(landscape, rain, n_pollution, w_pollution, e_pollution, s_pollution,
                     n_wind_direction, w_wind_direction, e_wind_direction, s_wind_direction):
    counter = 0
    if rain:
        counter -= 3
    if landscape == 'Forest':
        counter -= 1
    if landscape == 'City':
        counter += 2

    if n_wind_direction == 'v':
        if n_pollution:
            counter += 1
    if s_wind_direction == '^':
        if s_pollution:
            counter += 1
    if e_wind_direction == '<':
        if e_pollution:
            counter += 1
    if w_wind_direction == '>':
        if w_pollution:
            counter += 1
    return counter > 0


# Temp is increased by pollution and by sunny days (no clouds).
# Decreases by a clear or clouded city and ice.
# On the edges of the temp's range it is also affected by its neighbors' temps.
def update_temp(landscape, clouds, pollution, prev_temp, temps):
    temp = prev_temp
    if pollution:
        temp += 2
    elif landscape == 'City':
        temp -= 1
    if landscape != 'Ice':
        if clouds:
            temp -= 2
            if landscape == 'City':
                temp -= 4
        else:
            temp += 1
    if temp > MAX_TEMP:
        temp = MAX_TEMP
    elif temp < MIN_TEMP:
        temp = MIN_TEMP

    avg = int(sum(temps) / len(temps))
    diff = avg - prev_temp
    if temp == MAX_TEMP or temp == MIN_TEMP:
        temp = temp + int(diff / 4)

    return temp


# Clouds are created by the sea and drifts on the wind.
# They cease to exist after rainfall.
def update_clouds(rain, clouds, wind_speed, landscape,
                  n_clouds, s_clouds, e_clouds, w_clouds,
                  n_wind_direction, s_wind_direction, e_wind_direction, w_wind_direction):
    if rain:
        return False
    else:
        if clouds:
            if wind_speed == 0:
                return True
        else:
            if landscape == 'Sea':
                return True
            else:
                if n_wind_direction == 'v':
                    if n_clouds:
                        return True
                if s_wind_direction == '^':
                    if s_clouds:
                        return True
                if e_wind_direction == '<':
                    if e_clouds:
                        return True
                if w_wind_direction == '>':
                    if w_clouds:
                        return True
    return False


# Warm ice will turn to sea and cold sea to ice.
# Sea level rises as icebergs melt and can flood nearby lower cells.
# Height changes only when neighboring sea cells has different heights to their average.

def landscape_and_height_update(prev_landscape, prev_height, prev_temperature, landscapes, heights):
    if prev_landscape == 'Ice':
        if prev_temperature < 10:
            return 'Ice', prev_height
        else:
            return 'Sea', prev_height
    if prev_landscape == 'Sea':
        if prev_temperature >= -20:
            # calculate average sea height
            sea_sum = prev_height
            sea_num = 1
            for i in range(len(landscapes)):
                if landscapes[i] == 'Sea':
                    sea_sum += heights[i]
                    sea_num += 1
            return 'Sea', int(sea_sum / sea_num)
        else:
            return 'Ice', prev_height
    else:
        if 'Sea' not in landscapes:
            return prev_landscape, prev_height
        else:
            for i in range(len(landscapes)):
                if heights[i] > prev_height:
                    if landscapes[i] == 'Sea':
                        if heights[i] > 9 * prev_height:
                            return 'Sea', prev_height
    return prev_landscape, prev_height
