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


  
