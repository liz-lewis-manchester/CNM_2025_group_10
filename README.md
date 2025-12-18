Notes about our repository:

CNM_Group_10_coursework.ipynb contains all our tests (what the instructions in this read me follows). Note, to see test 3 code you have to open directly with collab as opposed to just viewing in github. Note not in notebook folder due to issues with loosing files.

Copy_of_CNM_Group_10_coursework.ipynb contains our code in a notebook, without individual tests. Note not in notebook folder due to issues with loosing files.

model.py is our combined code in python form.

Other .py files are outdated and are no longer used in the model.



Main code and test case 1:

Four required libraries are imported: numpy, pandas, matplotlib.pylot, and matplotlib.animation.
The function 'define_domain()' creates the spatial grid representing distance along the river and the temporal grid representing the simulation time. The domain limits and step sizes are defined as function arguments, allowing the domain to be easily modified if required.

Model parameters are stored using 'define_parameters()', which currently returns the advection velocity 'U'.

Importing and interpolating the initial conditions required for test two:

The data provided is based on initial conditions therefore the data must show the concentration at each distance at t=0. These concentration values will be the initial theta values for test two. This task involved converting the provided data into a form that can be used in calculations.

A ‘get_initial_conditions_from_CSV’ function is defined using the initial conditions CSV file as well as given x and dx values from instructions. Within this function, pandas, is used to read in the initial conditions which have been added to the repository. Note, ‘encoding=latin1’ was used to prevent an error. Distance and concentration columns are extracted and defined from the CSV file, and a model spatial grid is made. ‘Interp’ from numpy is used to make the initial conditions meet the domain. An exception is used if there is an error in the CSV file. 

The initial pollutant concentration depends on the test type and the code is set up to allow the user to choose. For all the test cases the temporal and spatial grid points have to go from zero, to whatever the user chooses as the maximum length (L) and time (T), with steps (dx and dt respectively) defined by the user. The pollutant array is also initialised here with u_initial = np.zeros(Nx). The ‘configure_simulation()’ includes a test_case_id argument. For test 1, the test_case_id is 1 (or the user should input 1), and the initial pollutant is 250.

Within ‘if’ test case 1 plays, within ‘elif’ test case 2 plays. The CSV data read in during the ‘get_initial_conditions_from_csv()’, is defined as csv_data. If this is without error, this csv data becomes u_initial. If there is an error with the read in, a fall back involving manually provided conditions is included. Additionally, if there is an error with the case ID chosen an error is raised.
‘configure_simulation()’ returns then all data necessary for the solver.

The code to model concentration is defined as run_solver. The initial condition is set with u=0 and the concentration at each time and a space will be stored in the config dictionary. The ‘for k in range (1, Nt)’ is a time loop calculating the concentration at each time. Code adds the option to add a random permutation as will be necessary in later tests. Considering any possible change in velocity, values for A and B are created, depending on what parameters for dx and dt are provided by user. While the previous code calculates time loop, ‘for I in range (1, Nx)’ calculates the concentration at each point based on the concentration at the previous. The code also includes the opportunity to add a decay constant which would be necessary in later tests. 

U[k, :] saves the concentration at each time point into a solution array. 

U is the full concentration field for animating. 

Animate_solutions is a function that shows the changing concentrations at each point in a river over time. First the axes are cleared, then concentration against distance at each time frame is plotted. The axes are limited with x from 0 to maximum distance, and concentration (y axis) from zero to slightly above maximum concentration found in calculations. The axes are labelled and the plot titled. Grid lines are added for readability. ‘animation.FuncAnimation’ calls the function at each frame based on the time step provided by user. 

Finally, code allows for the user to choose their own parameters. When you click play, the user will be prompted for each parameter after another. 

Test case 2:

Input test_case_id = 2 to get CSV initial conditions. 

Test Case 3-5:

Involve changing various parameters as shown in code and the user can vary these at will. 
