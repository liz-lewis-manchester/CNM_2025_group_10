theta_new=np.zeros(Nx)  #creates empty array for theta_new
F=np.zeros(Nx-1)  #creates empty array for right-hand side vector F  
theta=np.zeros((Nt, Nx))  #creating empty array to store all the values of concentration over time and space
theta[0,:]=theta_old  #initial concentration at t=0 is stored in the first row
import random  #importing the random module
#here we create an outer time stepping loop to perform our calculations:
def loop(test_case_id, random_perturbation, decay_constant, U, Nt, Nx, dx, dt, A, B, F, theta_old, theta_new):
  for j in range(1,Nt+1):
    if test_case_id==4:  #for test 4 we will compute the effects of exponential decay on the initial concentration
      theta_new[0]=theta_old[0]*(1-decay_constant)^dt
    else:
      theta_new[0]=theta_old[0]  #otherwise the concentration remains constant and we set the value of theta_new[0] to the given initial condition
#next we create an inner loop which loops over the values in space:
    for i in range(0,Nx-1):
      if test_case_id==5:  #for test 5 we will add a random perturbation to the constant velocity:
        U_perturbed = U * (1 + random.uniform(-random_perturbation/100, random_perturbation/100))
        a=1/dt+U_perturbed/dx  #recomputing the coefficients a and b as well as the arrays A and B
        b=-1*U_perturbed/dx
        A=np.ones(Nx-1)*a
        B=np.ones(Nx-1)*b
      F[i]=1/dt*theta_old[i+1]  #calculate the values of F 
      theta_new[i+1]=1/A[i]*(F[i]-B[i]*theta_new[i])  #Solve for theta_new to find the concentration for a particular time step
    theta[j,:]=theta_new  #store the current concentration in row j of theta for each iteration
    theta_old=theta_new  #update the value of theta_old to prepare for the next loop
  return theta  #return all concentration values over time and space
