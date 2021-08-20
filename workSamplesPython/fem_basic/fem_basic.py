'''

* The following program uses the finite difference method to solve a simple 1-D transient heat conduction problem.

	Problem:	A 0.1 meter long steel rod is initially at uniform temperature 25 deg celsius. It is, now, heated by 
				maintaining one side at 50 deg celsius and the other at 30 deg celsius. Use FDM to solve the problem.
				Assume thermal diffusivity alpha of steel to be 10^-5 m^2/s.  
			
* The program's complete lack of user interface will make it difficult for the user to try new problems.
* I have made as many comments as i can, to help the user understand the program though. 

'''

# import matplotlib.pyplot for plotting our results
import matplotlib.pyplot as plt

# change these things as required by the problem
X_BOUNDS = (-0.05, 0.05)		# the range of x values
T_BOUNDS = (0.0, 5*60.)			# the range of t values 
ALPHA = 1e-5					# material property... you might want to change this

# hyperparameters you might want to tune for good results
NO_OF_X_POINTS = 25			# keep this greater than 1
NO_OF_T_POINTS = 1000		# keep this greater than 1 and much greater in fact... 
							# ...low values will cause the numbers to explode and become unstable

# the time step and grid spacing are determined by the program... indirect control is given to user through NO_OF_XXX parameters
DELTA_T = (T_BOUNDS[1] - T_BOUNDS[0]) / (NO_OF_T_POINTS - 1)
DELTA_X = (X_BOUNDS[1] - X_BOUNDS[0]) / (NO_OF_X_POINTS - 1) 

# TEMP_XXX dicts are used to store temperature values at different positions and times...
# all TEMP_XXX dicts use tuple (discrete_x, disctrete_y) as keys... 
TEMP_INITIAL_CONDITIONS = {}		# will store the initial conditions

# using a simple loop, i have specified the initial conditions as all points having the same temperature 0 deg celsius 
# you might want to change this to try a different problem...
# it is not as straightforward though most of the times...
for discrete_x in range(2, NO_OF_X_POINTS):
	TEMP_INITIAL_CONDITIONS[(discrete_x, 1)] = 25

# here, i have specified the boundary conditions as one side is maintained at 20 deg celsius...
# ...and the other side at 50 deg celsius
# you might want to change this when solving a different problem...
# take care not to write conditions overlapping with the initial conditions
# in case of overlap, boundary conditions will write over the initial conditions where overlap occurs
TEMP_BOUNDARY_CONDITIONS = {}
for discrete_t in range(1, NO_OF_T_POINTS + 1):
	TEMP_BOUNDARY_CONDITIONS[(1, discrete_t)] = 50
	TEMP_BOUNDARY_CONDITIONS[(NO_OF_X_POINTS, discrete_t)] = 30


# TEMP_AT_DISCRETE_POINTS pulls values from the initial conditions and boundary conditions...
# this dict will be storing values of temperature that are calculated later
TEMP_AT_DISCRETE_POINTS = {}
TEMP_AT_DISCRETE_POINTS.update(TEMP_INITIAL_CONDITIONS)
TEMP_AT_DISCRETE_POINTS.update(TEMP_BOUNDARY_CONDITIONS)


# function that calculates and returns the temperature for a given (discrete_x, discrete_t)
# the understanding of what this function does is not necessary for the user 
# it uses the finite difference method to calculate the temperature at the new point
# it seeks some values that are required for the calculation from the TEMP_AT_DISCRETE_POINTS dict
# it throws an error if they have not been calculated yet 
def calculate_temp_for_discrete_point(discrete_point):
	discrete_x, discrete_t = discrete_point
	temp_i_1k = TEMP_AT_DISCRETE_POINTS[(discrete_x, discrete_t - 1)]
	temp_i1_1k = TEMP_AT_DISCRETE_POINTS[(discrete_x + 1, discrete_t - 1)]
	temp_1i_1k = TEMP_AT_DISCRETE_POINTS[(discrete_x - 1, discrete_t - 1)]
	temp_i_k = temp_i_1k + ((ALPHA * DELTA_T) / DELTA_X ** 2) * (temp_i1_1k - 2 * temp_i_1k + temp_1i_1k) 
	return temp_i_k

# calculating temperature values for different (discrete_x, discrete_t) by calling the above function
# it, then, writes these values to the TEMP_AT_DISCRETE_POINTS dict 
for discrete_t in range(2, NO_OF_T_POINTS + 1):
	for discrete_x in range(2, NO_OF_X_POINTS):
		TEMP_AT_DISCRETE_POINTS[(discrete_x, discrete_t)] = calculate_temp_for_discrete_point((discrete_x, discrete_t))


# finding the range of temperature values that have been encountered
# used in the plotting helper functions 
min_temp_in_TEMP = min(TEMP_AT_DISCRETE_POINTS.values())
max_temp_in_TEMP = max(TEMP_AT_DISCRETE_POINTS.values())
temp_in_TEMP_range = max_temp_in_TEMP - min_temp_in_TEMP

# plotting helper functions... The values we calculate are in blue... values that were supplied such 
# as the initial conditions and boundary conditions are in red...
# plots temerature distributuon given time as t or discrete_t... 
# if you are supplying discrete_t, use True as argument for 'discrete' parameter
def plot_temp_distribution(time, discrete = False):		
	if discrete == False:
		discrete_t = round((time - T_BOUNDS[0]) / DELTA_T) + 1
	else:
		discrete_t = time
		time = (discrete_t - 1) * DELTA_T + T_BOUNDS[0]
	x = []
	temp = []
	for discrete_x in range(1, NO_OF_X_POINTS + 1):
		x.append((discrete_x - 1) * DELTA_X + X_BOUNDS[0])
		temp.append(TEMP_AT_DISCRETE_POINTS[(discrete_x, discrete_t)])
	plt.plot(x[0], temp[0], color='red', marker='x')
	color_ = 'blue'
	if discrete_t == 1:
		color_ = 'red'
	plt.plot(x, temp,color=color_) 
	plt.plot(x[-1], temp[-1], color='red', marker='x') 
	plt.grid()
	plt.title(f'temperature_distribution_@_time {round(time, 3)} s') 
	plt.xlabel('position_x(in m)')
	plt.ylabel(u'temperature(in \N{DEGREE SIGN}C)')
	plt.ylim(min_temp_in_TEMP - .1 * temp_in_TEMP_range, max_temp_in_TEMP + .1 * temp_in_TEMP_range)
	plt.show()

# plots temerature evolution given position as x or discrete_x... 
# if you are supplying discrete_x, use True as argument for 'discrete' parameter
def plot_temp_evolution(x, discrete = False):	
	if discrete == False:
		discrete_x = round((x - X_BOUNDS[0]) / DELTA_X) + 1
	else:
		discrete_x = x
		x = (discrete_x - 1) * DELTA_X + X_BOUNDS[0]
	t = []
	temp = []
	for discrete_t in range(1, NO_OF_T_POINTS + 1):
		t.append((discrete_t - 1) * DELTA_T + T_BOUNDS[0])
		temp.append(TEMP_AT_DISCRETE_POINTS[(discrete_x, discrete_t)])
	plt.plot(t[0], temp[0], color='red',marker='x')
	color_ = 'blue'
	if discrete_x == 1 or discrete_x == NO_OF_X_POINTS:
		color_ = 'red'
	plt.plot(t, temp, color=color_)
	plt.grid()
	plt.title(f'temperature_evolution_@_position {round(x, 3)} m') 
	plt.xlabel('time(in s)')
	plt.ylabel(u'temperature(in \N{DEGREE SIGN}C)')
	plt.ylim(min_temp_in_TEMP - .1 * temp_in_TEMP_range, max_temp_in_TEMP + .1 * temp_in_TEMP_range)
	plt.show()

# testing
# we test the program by making a few plots of both types
# plots temperature against position for different times
# times are selected using a logarithmic scale... 
# this is done to make sure the user is not seeing mostly similar plots toward the end...
# ...as the temperatures become steady 
plot = True 		# to plot or not
no_of_plots = 5		# number of plots to make... keep this greater than 1
if plot == True:
	k = NO_OF_T_POINTS ** (1 / (no_of_plots - 1))
	for i in range(no_of_plots):
		plot_temp_distribution(round(1 * k ** i), discrete=True)

# plots temperature against time for different positions
# positions are selected with same distance between each other
plot = True		# to plot or not
no_of_plots = 5		# number of plots to make... keep this greater than 1
if plot == True:
	for i in range(no_of_plots):
		plot_temp_evolution(X_BOUNDS[0] + i * (X_BOUNDS[1] - X_BOUNDS[0]) / (no_of_plots - 1))