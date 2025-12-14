#Information on labelling:
#initial_conditions = data from canvas
#theta_preinterpol = initial conditions in matrix form
#distance = Distance (m) in 1D series form
#concentration = Concentration (µg/m_ ) in 1D series form
#theta_preinterpol_series = initial conditions combined into series form, before any interpolation
#distance_index = distance column in domain provided form
#theta_NaNs = concentration adjusted to have gaps in column
#theta_NaNs_interpolated = concentration column fully interpolated
#theta_old = concentration in form ready for calculations

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

distance_index = np.linspace(0, 20, 101) #interpolating distance

theta_NaNs=theta_preinterpol_series.reindex(distance_index) #interpolating concentration part 1
theta_NaNs_interpolated = theta_NaNs.interpolate(method='linear') #interpolating concentration part 2

#based on test 2, this will be produced as the value for theta_old
theta_old = theta_NaNs_interpolated.values.reshape(-1, 1) #putting theta_old into a form that can be used in calculations
