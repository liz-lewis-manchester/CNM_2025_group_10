import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Domain and Parameters

def define_domain(x_start=0.0, x_end=20.0, dx=0.2,
                  t_start=0.0, t_end=300.0, dt=10.0):
    #creates a spatial grid with spacing dx
    x = np.arange(x_start, x_end + dx, dx)
    #creates a time grid with spacing dt
    t = np.arange(t_start, t_end + dt, dt)
    #returns the grids for use in the solver
    return x, t, len(x), len(t)

def define_parameters(U=0.1):
  #return the flow velocity
    return U

# Initial Conditions
def get_initial_conditions_from_csv(csv_file='initial_conditions.csv', L=20.0, dx=0.2):
    try:
        #reads the csv file
        df = pd.read_csv(csv_file, encoding='latin1')
        #extracts the distance and concentration columns
        distance = df['Distance (m)'].values
        concentration = df['Concentration (µg/m_ )'].values
        #creates a model spatial grid
        x_grid = np.arange(0, L + dx, dx)
        #this interpolates the concentration values onto the model grid
        #this then allows the initial conditions to match the numerical domain
        return np.interp(x_grid, distance, concentration)
    except Exception as e:
      #handles errors like missing files or incorrect file names
        print(f"CSV read failed: {e}")
        return None

# Simulation Configuration

def configure_simulation(test_case_id, L=20.0, T=300.0, dx=0.2, dt=10.0, U=0.1):
  #number of spatial and temporal grid points
    Nx = int(L / dx) + 1
    Nt = int(T / dt) + 1
  #creates the temporal and spatial grid points
    x_grid = np.linspace(0, L, Nx)
    t_grid = np.linspace(0, T, Nt)
  #initialises the pollutant concentration array
    u_initial = np.zeros(Nx)

#test case 1 - Pulse release
    if test_case_id == 1:
#sets initial concentration at only x=0
        u_initial[0] = 250.0
#test case 2 - initial conditions from csv file
    elif test_case_id == 2:
        csv_data = get_initial_conditions_from_csv(L=L, dx=dx)
        if csv_data is not None and len(csv_data) == Nx:
            u_initial = csv_data
        else:
#fallback profile if the csv reading fails
            print("CSV failed, using fallback profile")
            csv_distance = [0, 5, 10, 15, 20]
            csv_concentration = [250, 50, 20, 10, 0]
            u_initial = np.interp(x_grid, csv_distance, csv_concentration)
#raise an error if the test case is invald
    else:
        raise ValueError(f"Test Case {test_case_id} not recognized")

#returns configurations for use in the solver
    return {
        'x': x_grid,
        't': t_grid,
        'u_init': u_initial,
        'velocity': U,
        'dx': dx,
        'dt': dt
    }

# Solver (recursive sweep)
def run_solver(config, decay_constant=0.0, random_perturbation=0.0,
               pulse_duration=3):
  #Implicit upwind solver for 1D advection with optional decay and optional velocity perturbation

#extracts the necessary grids and parameters
    x, t = config['x'], config['t']
    U, dx, dt = config['velocity'], config['dx'], config['dt']
    Nt, Nx = len(t), len(x)

#allocates an array to store concentration at all times and distances
    u = np.zeros((Nt, Nx))
#sets initial concentration profile at t=0
    u[0, :] = config['u_init']

#time stepping loop
    for k in range(1, Nt):
#create an array for the concentration at the current timestep
        concentration_present = np.zeros(Nx)

  #upstream boundary condition: finite pulse
  #a finite pulse is injected for a specified number of timesteps
  #once pulse ends, then clean water enters the domain/river
        if k <= pulse_duration:
            concentration_present[0] = u[0, 0] * np.exp(-decay_constant * k * dt)
        else:
            concentration_present[0] = 0.0

#velocity field
# Variable velocity with optional perturbation
        random_variable = np.random.random(Nx)
        random_speed = (1 - random_perturbation / 100
                        + random_perturbation / 50 * random_variable) * U

#coefficients for the implicit upwind scheme
        A_value = 1 / dt + random_speed / dx
        B_value = random_speed / dx

  #implicit upwind spatial sweep
  #concentration is updated sequentially from upstream to downstream using the previous timestep values
        for i in range(1, Nx):
            concentration_present[i] = (
                u[k - 1, i] / dt + B_value[i] * concentration_present[i - 1]
            ) / A_value[i]

        #apply decay everywhere (used for later test case)
        if decay_constant > 0.0:
            concentration_present *= np.exp(-decay_constant * dt)

#store concentration for this timestep
        u[k, :] = concentration_present

#return the full concentration field
    return u


# Animation
def animate_solution(x, t, u, interval=200):
#improves figure resolution
    plt.rcParams['figure.dpi'] = 150
#enable JavaScript-based animations (allows the graph to be seen in notebooks without having to call it forward)
    plt.rcParams["animation.html"] = "jshtml"
  #turns off the interactive plotting to avoid duplicate figures
    plt.ioff()

#create a figure with axes
    fig, ax = plt.subplots()

    def animate(frame):
#clears axes to redraw concentration profiles
        ax.cla()
#plots concentration along the river at current timestep
        ax.plot(x, u[frame, :])
#fits axis limits to ensure there is consistent scaling
        ax.set_xlim(0, x[-1])
        ax.set_ylim(0, np.max(u) * 1.1)
#labels the different axis
        ax.set_xlabel("Distance (m)")
        ax.set_ylabel("Concentration (μg/m³)")
        ax.set_title(f"Concentration at Time = {t[frame]:.1f} s")
#adds the grid to improve readability
        ax.grid(True)

#creates the animation by repeatedly calling the animation function
    anim = animation.FuncAnimation(fig, animate, frames=len(t), interval=interval)

#returns the animation object (this allows it to be saved easier)
    return anim

# Main with Input Parameters
#allows user to choose between simple pulse inlet with input parameters or reading from the csv file
if __name__ == "__main__":
    test_case_id = int(input("Enter test case (1=pulse, 2=CSV): "))
    L = float(input("Enter river length (m): ")) #total length of the river
    T = float(input("Enter simulation time (s): ")) #total time for the simulation
    dx = float(input("Enter spatial resolution (m): ")) #the increment of distance on the graph
    dt = float(input("Enter time step (s): ")) #the increment of time on the graph
    U = float(input("Enter velocity (m/s): ")) #the flow velocity
    decay_constant = float(input("Enter decay constant (e.g., 0.0 for none): ")) #used for later test cases and adds pollutant decay
    random_perturbation = float(input("Enter random perturbation % (0 for none): ")) #used for later test cases and adds random velocity variation

    config = configure_simulation(test_case_id, L=L, T=T, dx=dx, dt=dt, U=U) #configures the intial conditions and figure simulation based on selected test
    u = run_solver(config, decay_constant=decay_constant, random_perturbation=random_perturbation) #runs the solver to compute the concentration of pollutant over space and time
    anim_result = animate_solution(config['x'], config['t'], u) #animates the results

#displays animation inline (so it can be seen in the notebook)
    from IPython.display import HTML
    display(HTML(anim_result.to_jshtml()))
