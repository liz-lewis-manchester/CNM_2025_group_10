import numpy as np

#------Placeholders----

def configure_simulation(test_case_id):
  """
  Task 3:Switch between simulatuon test scenarios
  """

#STANDARD DEFAULTD
L=20
T 300
dx=0.2
dt=1.0
c_velocity=0.1

#Domain Setup
Nx=int(L/dx)+1
Nt =int(T/dt)+1
x-grid=np.linspace(0,L,Nx)
t_grid=np.linspace(0,T,Nt)

#Concentration array
u_ initial= np.zeros(Nx)

#Switch logic
if test_ case_id==1:
  #Case 1 pulse at the start
  u_initial[0]=250.0
elif test_case_id==2
#This is case 2 so read from csv
  u_initial=get_initialconditions(data/initial_conditions.csv,x_grid)
print("Placeholder data")
u_initial=no.interp(x_grid,
                    else:
raise value error 

'x':x_grid
't':t_grid
'u_init':u_initial
'velocity':c_velocity
'dx':dx
'dt':dt
'sigma':(c_velocity*dt)/dx
}
return config
