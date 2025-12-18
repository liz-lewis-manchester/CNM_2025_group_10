import numpy as np
import pandas as pd

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

# This function reads the csv file and interpolates the data
def get_initial_conditions_from_csv():
    try:
        initial_conditions = pd.read_csv('initial_conditions.csv', encoding='latin1')
        theta_preinterpol = initial_conditions[['Distance (m)', 'Concentration (µg/m_ )']].values
        distance = theta_preinterpol[:, 0]
        concentration = theta_preinterpol[:, 1]
        
        theta_preinterpol_series = pd.Series(concentration, index=distance)
        distance_index = np.linspace(0, 20, 101)
        
        theta_NaNs = theta_preinterpol_series.reindex(distance_index)
        theta_NaNs_interpolated = theta_NaNs.interpolate(method='linear')
        
        return theta_NaNs_interpolated.values
    except:
        return None

# This function configures the simulation based on the test case ID
def configure_simulation(test_case_id):

    # Standard model defaults
    L = 20.0
    T = 300.0
    dx = 0.2
    dt = 1.0
    c_velocity = 0.1

    # Domain Setup
    Nx = int(L / dx) + 1
    Nt = int(T / dt) + 1
    
    x_grid = np.linspace(0, L, Nx)
    t_grid = np.linspace(0, T, Nt)

    # Concentration array
    u_initial = np.zeros(Nx)

    # Switch logic for test cases
    if test_case_id == 1:
        # Case 1: Pulse at the start
        u_initial[0] = 250.0

    elif test_case_id == 2:
        # Case 2: Read from CSV
        print("Configuring Test Case 2 (Real Data)...")
        
        csv_data = get_initial_conditions_from_csv()
        
        if csv_data is not None and len(csv_data) == Nx:
             u_initial = csv_data
        else:
             # Fallback to manual data if CSV fails
             print("Using manual data points (CSV fallback)")
             csv_distance = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 12.35, 13.57, 14.80, 15.85, 16.00, 17.50, 18.40, 19.20, 20.10]
             csv_concentration = [300, 10, 10, 10, 10, 8, 8, 8, 8, 7, 7, 10.7, 11.7, 12.35, 13.57, 14.80, 15.85, 16.00, 17.50, 18.40, 20.10]
             u_initial = np.interp(x_grid, csv_distance, csv_concentration)

    else:
        raise ValueError(f"Test Case {test_case_id} not recognized")

    # Pack configuration into dictionary
    config = {
        'x': x_grid,
        't': t_grid,
        'u_init': u_initial,
        'velocity': c_velocity,
        'dx': dx,
        'dt': dt,
        'sigma': (c_velocity * dt) / dx
    }
    
    return config

if __name__ == "__main__":
    try:
        data = configure_simulation(2)
        print("Setup Successful")
    except Exception as e:
        print(e)
        
#Interpolation defined differently, once we have complete code will need to be made consistent so reminder to adjust here.
#Also note different indents used.
  
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

def animate(i):
  plt.cla() #clear previous view
  #here I would need data produced from calculations but for now I will use "theta.coming" as the array being produced from the calculation. This will be altered once calculation is added to main branch.
  theta=theta_coming[i,:]
  plt.plot(x, theta) #setting up plot
  plt.xlim(x_start,x_end) #x axis limits defined ealier as provided by either the question or initial conditions.
  plt.ylim(0,theta_coming.max()) #y axis limits from zero to the maximum value of theta from the calculations.
  #graph labels
  plt.xlabel("Distance (m)")
  plt.ylabel("Concentration (μg/m³)")
  plt.title("Modelling pollutant transport in a river")
  #t counter
  plt.annotate(f"t = {t[i]:.1f} s", xy=(0.05, 0.95), xycoords="axes fraction")

anim = matplotlib.animation.FuncAnimation(fig, animate, frames=len(t))
anim
