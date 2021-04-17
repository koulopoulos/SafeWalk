import numpy as np
import pandas as pd
import os
from scipy import stats

df = pd.read_csv("crime.csv")
streets = []
class Street:
    def __init__(self, name, num_crimes):
        self.name = name
        self.num_crimes = num_crimes
        self.weight = 0
    def init_weight(self):
        self.weight = self.num_crimes

num_crimes = df['STREET'].value_counts()
street_names = df['STREET'].drop_duplicates()
for name in street_names:
    streets.append(Street(name, num_crimes.get(name)))
for street in streets:
    street.init_weight()
    print(street.weight)
