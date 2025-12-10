#Interpolating for test 2:
import pandas as pd #pandas library is needed to import csv file
initial_conditions = pd.read_csv('initial_conditions.csv', encoding='latin1') #reading in file
#the encoding is there to remove the UnicodeDecodeError that is produced without it

import numpy as np #numpy library needed for matrices
theta_preinterpol=initial_conditions[['Distance (m)', 'Concentration (µg/m_ )']].values #making the initial conditions into a matrix

#to apply interpolation, data needs to be in a series form so take take distance and concentration (still in non interpolated form)
distance = theta_preinterpol[:, 0] #distance in columnn zero (aka column 1 in general speak)
concentration = theta_preinterpol[:, 1] #concentration in column one (aka column 2 in general speak)
# create a Series where:
theta_preinterpol_series = pd.Series(concentration, index=distance)
