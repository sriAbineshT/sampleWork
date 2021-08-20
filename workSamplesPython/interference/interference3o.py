import math,pygame,sys
from pygame.locals import *

pi=3.141592653589793

def lin_space(start,finish,step):#generates list with values in range with given step...includes start and finish
	z_list=[]
	z=start
	if step>0:
		while z<=finish:
			z_list.append(z)
			z+=step
	elif step<0:
		while z>=finish:
			z_list.append(z)
			z+=step
	return z_list

source_list=[[(0,-.5,10),1,0],[(0,.5,10),1,0]]
source_wavelength=.1


def find_distance(pt1,pt2):
	return ((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2+(pt1[2]-pt2[2])**2)**.5

def find_amplitude_at_pt(point):
	vector_result=(0,0)
	for source in source_list:
		distance=find_distance(source[0],point)
		vector_magn=source[1]/distance
		vector_phase=source[2]+(distance*(2*pi/source_wavelength))
		vector=(vector_magn*math.cos(vector_phase),vector_magn*math.sin(vector_phase))
		vector_result=(vector[0]+vector_result[0],vector[1]+vector_result[1])
	return (vector_result[0]**2+vector_result[1]**2)**.5	

#generates a 2D list with 3D points in the rect described by pt1 and pt2...the rect is on the x-y plane...always...it wont be necessary to have pt1 and pt2 to be 3D...pt1 is the bottom left and pt2 is the top right of the rect
def plane_space(pt1,pt2,step): 
	x_space=lin_space(pt1[0],pt2[0],step)
	y_space=lin_space(pt2[1],pt1[1],-step)
	xy_list=[]
	for y in y_space:
		row=[]
		for x in x_space:
			row.append((x,y,0))
		xy_list.append(row)
	return xy_list
	
screen_pts=plane_space((-8,-5),(8,5),.01)#same y values are put in a row
scr_width=len(screen_pts[0])#no of elements in a row
scr_height=len(screen_pts)#no of rows	
	
#find amplitudes for all points on screen
amplitude_at_pt=[]
max_amplitude=0
for screen_row in screen_pts:
	amp_row=[]
	for screen_pt in screen_row:
		amplitude=find_amplitude_at_pt(screen_pt)
		if amplitude>max_amplitude:
			max_amplitude=amplitude
		amp_row.append(amplitude)
	amplitude_at_pt.append(amp_row)

pygame.init()

DISPLAYSURF=pygame.display.set_mode((scr_width,scr_height))
pygame.display.set_caption('interference3pointO')

pixObj=pygame.PixelArray(DISPLAYSURF)
for scr_row in range(0,scr_height):#scr_row index will actually be the y val on screen and scr_col index is x of the screen
	for scr_col in range(0,scr_width):
		gray=int(amplitude_at_pt[scr_row][scr_col]*255/max_amplitude)
		pixObj[scr_col][scr_row]=(gray,gray,gray)
del pixObj

pygame.display.update()

while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
	


