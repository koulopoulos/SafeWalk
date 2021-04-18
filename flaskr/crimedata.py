import numpy as np
import pandas as pd
import os
data = pd.read_csv("crime.csv")
# subset of total data
df = data[data['YEAR'] == 2018]
crimes = []
class Crime:
    type = ""
    posn = (0, 0) 
    def __init__(self, type, posn, dangerous, time):
        self.type = type
        self.dangerous = dangerous
        self.posn = posn
        self.time = time
posns = df['Location']
offenses = df['OFFENSE_CODE_GROUP']
times = df['HOUR']
shootings = df['SHOOTING']

for index, row in df.iterrows():
    if shootings[index] == "Y":
        crimes.append(Crime(offenses[index], eval(posns[index]), True, times[index]))
    else:
        crimes.append(Crime(offenses[index], eval(posns[index]), False, times[index]))
    
# radius in degrees
def get_num_crimes_in_radius(posn, prev_pos, time):
    num_crimes_in_radius = 0
    dangerous_crimes = 0
    for crime in crimes:
        time_range = (crime.time-5, crime.time+5)
        if within_bounds(posn, prev_pos, crime.posn) and int(time) >= time_range[0] and int(time) <= time_range[1]:
            num_crimes_in_radius = num_crimes_in_radius + 1
            if crime.type == "Homicide":
                num_crimes_in_radius = num_crimes_in_radius + 25
            if crime.type == "Simple Assault" or crime.type == "Aggravated Assault":
                num_crimes_in_radius = num_crimes_in_radius + 5
            if crime.dangerous:
                dangerous_crimes = dangerous_crimes + 1

    return num_crimes_in_radius, dangerous_crimes

def within_bounds(posn1, posn2, posn3):
    return get_distance(posn3, posn1) + get_distance(posn3, posn2) < get_distance(posn1, posn2) + 0.0005
def get_distance(posn1, posn2):
    return np.sqrt((posn1[0] - posn2[0])**2 + (posn1[1] - posn2[1])**2)
    
def get_data(posn, radius, time):
    return get_num_crimes_in_radius(posn, radius, time)


