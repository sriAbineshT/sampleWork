##double slit interference
##a list that stores the positions of sources,all sources are in the same phase and have the same global wavelength and same global amplitude,ok?
import math
import matplotlib.pyplot as plt
import pygame,sys
from pygame.locals import *

def lin_space(start,finish,step):##generates list with values in range with given step
	z_list=[]
	z=start
	while z<=finish:
		z_list.append(z)
		z+=step
	return z_list

source_pos_list=[]

##source_pos_list=[(0,-1)]##single source

##source_pos_list=[(-1,-1),(1,-1)]##two sources

for val in lin_space(-1,1,2):
	source_pos_list.append((val,-2))


for source_pos in source_pos_list:
	plt.plot(source_pos[0],source_pos[1],'ro')
source_wavelength=.5
source_amplitude=1

pi=3.1415926536

def find_dist(posA,posB):##gives dist given two positions
	return ((posA[0]-posB[0])**2+(posA[1]-posB[1])**2)**.5

def find_phase(source_pos,point_loc):##returns phase angle given source pos and point loc del_theta=dist*2pi/wavelength
	return find_dist(source_pos,point_loc)*(2*pi/source_wavelength)

##to find result amplitude,find vector equivalents of the sources,cal the resultant and find its magn, a vector equivalent is each souces amp with its phase at a loc

def find_vector(magn,angle_in_rad):##given angle and magn finds corresponding vector 
	return (magn*math.cos(angle_in_rad),magn*math.sin(angle_in_rad))

def add_vect(vectA,vectB):##adds vectA to vectB
	return (vectA[0]+vectB[0],vectA[1]+vectB[1])

def find_amplitude(point_loc):##gives wave amplitude due to superposition of all sources at given pos
	init_vector=(0,0)
	for source_pos in source_pos_list:
		phase=find_phase(source_pos,point_loc)
		amp_new=source_amplitude/find_dist(source_pos,point_loc)##inverse reln bw dist and amp
		##amp_new=source_amplitude##assumption==no decrease in energy intensity with dist
		vector=find_vector(amp_new,phase)
		init_vector=add_vect(init_vector,vector)
	return find_dist(init_vector,(0,0))

##print(find_amplitude((1,2)))

##print(generate_points(0,5,1))

screen_points=lin_space(-15,15,.05)
amplitude_at_pt=[]

for point in screen_points:
	amplitude_at_pt.append(find_amplitude((point,0)))

plt.plot(screen_points,amplitude_at_pt)

print(len(screen_points))

pygame.init()

DISPLAYSURF=pygame.display.set_mode((len(screen_points),100))
pygame.display.set_caption('interference.py')

pixObj=pygame.PixelArray(DISPLAYSURF)

max=max(amplitude_at_pt)

for scrx in range(0,len(screen_points)):
	gray=int(amplitude_at_pt[scrx]*255/max)
	for scry in range(0,100):
		pixObj[scrx][scry]=(gray,gray,gray)
del pixObj

pygame.display.update()
plt.show()

while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()

	


