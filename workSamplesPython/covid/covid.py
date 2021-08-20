#creating an infection model to study how an infection spreads
#lets think of a rectangle with people living in small unit squares inside the rectangle this doesnt represent physical distancing
#the neighbors of a square are all squares having edge contact ie,. four 
#a square in contact with an infected gets infected nezt day
#i use z instead of x whenever possible coz i cant go to onboard every now and then
#lets begin by creating a 10*10 rect

#import required libraries
import matplotlib.pyplot as plt
import random

rect_height=7
rect_breadth=7

#create 2-D lists with all zeros
data_list=[]
gov_data_list=[]
for n in range(0,rect_height):
	row=[]
	row1=[]
	for nn in range(0,rect_breadth):
		row.append(0)
		row1.append(0)
	data_list.append(row)
	gov_data_list.append(row1)

#gov list will be modified based on the god list
#gov list key: 1=tested_positive 0=not_tested -2=tested_negative bw0and1=in_hospital_quarantine_and_treatment
#by the end of the day -2 will be be changed back to 0 
#god list key: 1=infected 0=not_infected -1=infected_today bw0and1=in_hospital_quarantine_and_treatment
#by end of day -1 will change into 0

#infect some guyz
data_list[3][3]=1

#parameters
infection_probability=.2

def infect_neighbors(self_pos):#changes neighboring 0s into -1s given self_pos
	#find neighbors
	neighbors_list=[]
	for rel_pos in [(-1,0),(0,-1),(1,0),(0,1)]:
		n_row=self_pos[0]+rel_pos[0]
		n_col=self_pos[1]+rel_pos[1]
		#if neighbor ezists,add neighbor
		if n_row in range(0,rect_height) and n_col in range(0,rect_breadth):
			neighbors_list.append((n_row,n_col))
	#change 0 to -1
	for neighbor_pos in neighbors_list:
		if data_list[neighbor_pos[0]][neighbor_pos[1]]==0:
			#introduce infection probability
			if random.random()<infection_probability:
				data_list[neighbor_pos[0]][neighbor_pos[1]]=-1		

def sim_a_day():#simulates a day
	#new infections 0-->-1
	for n in range(0,rect_height):
		for nn in range(0,rect_breadth):
			if data_list[n][nn]==1:
				infect_neighbors((n,nn))
	#change all -1 to 1
	for n in range(0,rect_height):
		for nn in range(0,rect_breadth):
			if data_list[n][nn]==-1:
				data_list[n][nn]=1

#data
day_list=[]
tot_infected_list=[]

def total_infected():#gives total number of infected cells
	tot_infected=0
	for n in range(0,rect_height):
		for nn in range(0,rect_breadth):
			if data_list[n][nn]==1:
				tot_infected+=1
	return tot_infected

def plot(z_azis,y_azis):
	plt.plot(z_azis,y_azis)
	plt.show()

def simulate(day_lim):#given number of days,runs simulation also stores data in lists
	for day in range(0,day_lim):
		#store required data
		day_list.append(day)
		tot_infected_list.append(total_infected())
		#simulate day
		sim_a_day()		

#test
simulate(10)
print(data_list)
print(gov_data_list)
plot(day_list,tot_infected_list)

#nezt task is to introduce medical help for infected people. lets say if a 1 pops up it gets medical help and its val is decremented slowly to reach 0 ie 
#perfect health. it keeps infecting people unless quarantined.to receive medical help,it must be tested positive.
#to simulate testing what do we do? we have to test all cells neighboring a positive infected cell and if eztra tests can be done it will happen randomly
#each day only a certain number of tests can be done
#for this we will have to create another list called the gov data list which will store data based on testing.
#what will it store? will it store the indez numbers of infected people?
#lets consider a list very similar to the actual list.the gov list starts with all zeros.then testing begins.the testing protocol will be as follows-
#once a cell is detected positive,its edge neighbors are tested if none are infected,testing moves on
#if some cell is detected positive ie with val 1,.... if val between 0 or 1 is found they are already being treated.
#a cell that tested negative ie 0 in god list will have val -2 in the gov list for that day.if a cell has val -2 in the gov list it will not be tested
#once a test is done.the value from the god list will be copied to gov list.
#testing protocol review...all cells that have values...


		
