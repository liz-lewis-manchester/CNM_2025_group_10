import numpy as np 

# This function sets up the river length and the time period we want to model
def define_domain(x_start=0.0, x_end=20.0, dx=0.2, t_start=0.0, t_end=300.0, dt=10.0):

  # Create the spatial grid (distance along the river)
  x = np.arange(x_start, x_end + dx, dx)

  # Create the time grid 
  t = np.arange(t_start, t_end + dt, dt)

  # Number of points in space and time
  Nx = len(x)
  Nt = len(t)

  return x, t, Nx, Nt

# This function stores the physical paramaters of the model 
def define_parameters(U=0.1):
  return U

# This function creates empty arrays for pollutant concentration 
def initialise_arrays(Nx):

  theta_old = np.zeros(Nx - 2)
  theta_new = np.zeros(Nx - 2)

  return theta_old, theta_new

# This function builds the constants needed for the finite difference scheme
def build_fd_coefficients(U, dx, dt, Nx):

  a = (1.0 / dt) + (U / dx)
  b = U / dx

  # Matrix used in the update step 
  A = np.eye(Nx - 2) * a

  # Vector used in the update step 
  B = np.ones(Nx - 2) * b

  return A, B


  
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
