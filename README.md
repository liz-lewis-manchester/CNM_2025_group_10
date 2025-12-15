Domain Definition and Model Setup:

This section defines the spatial and temporal domain for the model and sets up the core parameters and data structures required for the finite difference scheme.

The function 'define_domain()' creates the spatial grid representing distance along the river and the temporal grid representing the simulation time. The domain limits and step sizes are defined as function arguments, allowing the domain to be easily modified if required. 

Model parameters are stored using 'define_parameters()', which currently returns the advection velocity 'U'.

Initial arrays for pollutant concentration are created using 'initialise_arrays()', which generates empty arrays for the concentration at the previous and next time steps. 

The function 'build_fd_coefficients()' constructs the matrices and vectors required for the finite difference update step based on the spatial and temporal resolution and model parameters. These outputs are used by later stages of the model, including initial condition interpolation and time-stepping. 

Importing and interpolating the initial conditions required for test two:

The data provided is based on initial conditions therefore the data must show the concentration at each distance at t=0. These concentration values will be the initial theta values for test two. This task involved converting the provided data into a form that can be used in calculations.

This section begins with defining  what each variable means for clarity, before importing pandas, necessary for reading in the initial conditions which have been added to the repository. Note, ‘encoding=latin1’ was used to prevent an error when reading the initial conditions into the actual code. Following this, the canvas data provided is converted into a matrix using Numpy (which has previously been added to repository). Data is then converted into a series (theta_preinterpol_series) before an index of distance  (distance_index) can be made. As the data provided for distance is linear, it can be lined up with the domain using a linspace function where ‘(0,20,101)’ indicates the start, end, and number of values. 

Interpolating the concentration consists of two sections. The first is using the reindex function (based on information in the pandas data guide). It produces ‘NaNs’ where the four data points (at 0.2 intervals between the integers). The additional interval points had been previous produced in the linspace function. For example, 0.6m’s corresponding concentration is stored as ‘NaNs’. Next, the interpolate function is used to find the values of all the NaNs. From the data, corresponding distances and concentration levels are known when the distance is an integer so the values for non-integers (for example 0.2, 0.4, 0.6, and 0.8) are interpolated between these (for example 0 and 1). The interpolation assumes data points are linear between the two known integers’ concentrations. Finally the concentration data is converted into a form that can be used as the initial values of theta in the calculations.
