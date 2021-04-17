import numpy as np
import pandas as pd
import os
from scipy import stats

df = pd.read_csv("crime.csv")
crimes = []
class Crime:
    type = ""
    posn = (0, 0) 
    def __init__(self, type, posn):
        self.type = type
        self.posn = posn
posns = df['Location']
offenses = df['OFFENSE_CODE_GROUP']
for i in range(len(df)):
    crimes.append(Crime(offenses[i], eval(posns[i])))
# radius in degrees
def get_num_crimes_in_radius(posn, radius):
    num_crimes_in_radius = 0
    bad_crime_weight = 0
    for crime in crimes:
        dist = np.sqrt((crime.posn[0] - posn[0])**2 + (crime.posn[1] - posn[1])**2)
        if dist < radius:
            num_crimes_in_radius = num_crimes_in_radius + 1
            bad_crime_weight = bad_crime_weight + get_bad_crime_weight(crime)
    return num_crimes_in_radius
    
def get_weight(posn, radius):
    return get_num_crimes_in_radius(posn, radius)
print(get_weight((42.3, -71.1), 0.05))