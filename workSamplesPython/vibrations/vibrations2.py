def ON_OFF_function(a):
	if a<=0:
		return 0
	if a>0:
		return 1

def signum(a):
	if a<=0:
		return -1
	if a==0:
		return 0
	if a>=0:
		return 1

#computation parameters
time_step=.001
no_of_steps=10000

#system parameters
pos=0
vel=10
acc=0
time=0
mass=1
stiffness=1
damping_coeff=0
friction=.1

pos_list=[]
vel_list=[]
acc_list=[]
time_list=[]

for n in range(no_of_steps):
	pos_list.append(pos)
	vel_list.append(vel)
	acc_list.append(acc)
	time_list.append(time)
	force=(-stiffness*pos)+(-damping_coeff*vel)+(-friction*signum(vel))
	acc=force/mass
	d_vel=acc*time_step
	d_pos=vel*time_step
	vel+=d_vel
	pos+=d_pos
	time+=time_step

#plotting values in graph
import matplotlib.pyplot as plt
plt.plot(time_list,pos_list)
plt.show()


	
	
