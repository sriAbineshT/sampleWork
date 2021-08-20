import pygame, sys
from pygame.locals import *

GRAVITATIONAL_CONSTANT = 6.67430e-11	

# pick colors for planets; default color is WHITE
AQUA =      (  0, 255, 255)
BLACK =     (  0,   0,   0)
BLUE =      (  0,   0, 255)
FUCHSIA =   (255,   0, 255)
GRAY =      (128, 128, 128)
GREEN =     (  0, 128,   0)
LIME =      (  0, 255,   0)
MAROON =    (128,   0,   0)
NAVY_BLUE = (  0,   0, 128)
OLIVE =     (128, 128,   0)
PURPLE =    (128,   0, 128)
RED =       (255,   0,   0)
SILVER =    (192, 192, 192)
TEAL =      (  0, 128, 128)
WHITE =     (255, 255, 255)
YELLOW =    (255, 255,   0)

(WIN_W, WIN_H) = (1200, 600)		# window width and height; i wouldnt bother changing these

FPS = 10	# number of frames drawn per second; "more frames" means "more memory"
			# this is a lil tricky; if my computer cant pull the weight, simulation speed might become chaotic 
fpsClock = pygame.time.Clock()

planets_list = []	# every Planet object created gets added to this list

class Planet():
	def __init__(self, name=None, mass=5.972e24, color=BLUE, pos_x=0, pos_y=0, vel_x=0, vel_y=0, fixed=False):
		planets_list.append(self)
		self.name = name
		if self.name == None:
			self.name = f'EARTH#{id(self)}'
		self.mass = mass
		self.color = color
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.vel_x = vel_x
		self.vel_y = vel_y
		self.fixed = fixed
		if self.fixed == True:
			self.vel_x = 0
			self.vel_y = 0
		self.acc_x = 0
		self.acc_y = 0
		self.del_vel_x = 0
		self.del_vel_y = 0
		self.del_pos_x = 0
		self.del_pos_y = 0

	def find_and_set_acc(self):
		acc_x = 0
		acc_y = 0
		for planet in planets_list:
			if id(planet) != id(self):
				planet_pos_rel_self_x = planet.pos_x - self.pos_x
				planet_pos_rel_self_y = planet.pos_y - self.pos_y
				planet_dist = (planet_pos_rel_self_x ** 2 + planet_pos_rel_self_y ** 2) ** .5
				acc_magn = GRAVITATIONAL_CONSTANT * (planet.mass / planet_dist ** 2)
				acc_x_due_to_planet = acc_magn * (planet_pos_rel_self_x/ planet_dist)
				acc_y_due_to_planet = acc_magn * (planet_pos_rel_self_y/ planet_dist)
				acc_x += acc_x_due_to_planet
				acc_y += acc_y_due_to_planet
		self.acc_x = acc_x
		self.acc_y = acc_y
		if self.fixed == True:
			self.acc_x = 0
			self.acc_y = 0

	def calc_all_dels(self, del_time):
		self.find_and_set_acc()
		self.del_vel_x = self.acc_x * del_time
		self.del_vel_y = self.acc_y * del_time
		self.del_pos_x = self.vel_x * del_time
		self.del_pos_y = self.vel_y * del_time
		
	def update_all(self):
		self.vel_x += self.del_vel_x
		self.vel_y += self.del_vel_y
		self.pos_x += self.del_pos_x
		self.pos_y += self.del_pos_y

	def __str__(self):
		return f'name: {self.name}\nmass: {self.mass}\npos: ({self.pos_x}, {self.pos_y})\nvel: ({self.vel_x}, {self.vel_y})\nacc: ({self.acc_x}, {self.acc_y})'

def universal_delta_time(del_time):		# this is the god hand; moves the universe into the future by del_time
	for planet in planets_list:
		planet.calc_all_dels(del_time)
	for planet in planets_list:
		planet.update_all()

def COM():	# find the COM of all planets; used for testing
	COM_x = 0
	COM_y = 0
	total_mass = 0
	for planet in planets_list:
		COM_x += planet.mass * planet.pos_x
		COM_y += planet.mass * planet.pos_y
		total_mass += planet.mass
	COM_x /= total_mass
	COM_y /= total_mass
	return (COM_x, COM_y)

def create_surface_with_all(surf_dims, pixel_eq, scrn_center = (0, 0), bounding_rect_color=YELLOW):	
																	# looks up and draws all planets in the planets_list
																	# to a new Surface object; each pixel in the drawing
																	# is a square with side "pixel_eq" meters;
																	# the center of the drawing is aligned with 
																	# "scrn_center"; returns the Surface object 
	surface = pygame.Surface((surf_dims))
	for planet in planets_list:
		center_x = round((planet.pos_x - scrn_center[0]) / pixel_eq + (surf_dims[0] - 1)/2)
		center_y = round((planet.pos_y - scrn_center[1]) / pixel_eq + (surf_dims[1] - 1)/2)
		pygame.draw.circle(surface=surface, color=planet.color, center=(center_x, center_y), radius=8)
	pygame.draw.rect(surface=surface, color=bounding_rect_color, rect = surface.get_rect(), width = 1) 
	return surface

Planet(name='SUN', color=YELLOW, mass=1.989e30)
Planet(name='EARTH', color=BLUE, mass=5.976e24, pos_x=152.099e6 * 1000, vel_y=29.29 * 1000)
Planet(name='MOON', color=WHITE, mass=.07346e24, pos_x=152.099e6 * 1000 + 363_228.9 * 1000, vel_y=1.082 * 1000 + 29.29 * 1000)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption('PLANETS_SIMULATOR')

NO_PIXELS_TO_MOVE_DRAWING = 20
print(NO_PIXELS_TO_MOVE_DRAWING)

SIMULATION_SPEED = 24 * 3600	# when value is 1, simulation is in real time
								# simulation is faster for bigger values
								# increasing simulation speed doesnt cost memory
UDTs_PER_FRAME = 10_000	# number of calls to universal_delta_time() per frame; 
						# higher values lead to smoother calculations
						# costs memory
# (win_ctr_x, win_ctr_y) = (0, 0)		# to keep track of window_center in draw_all_planets()
									# will change during runtime to move around the drawing
scrn_ctr = [[0, 0], [0, 0]]
pixel_eq = [1e9, 1e9]
DUAL_SCREEN = True
SCREEN_CONTROL = 0
bounding_rect_color = [YELLOW, WHITE]

while True:
	DISPLAYSURF.fill(BLACK)
	for event in pygame.event.get():
		if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
			pygame.quit()
			sys.exit()
		elif event.type == KEYUP:
			if event.key == K_UP:
				scrn_ctr[SCREEN_CONTROL][1] -= NO_PIXELS_TO_MOVE_DRAWING * pixel_eq[SCREEN_CONTROL]
			elif event.key == K_LEFT:
				scrn_ctr[SCREEN_CONTROL][0] -= NO_PIXELS_TO_MOVE_DRAWING * pixel_eq[SCREEN_CONTROL]
			elif event.key == K_DOWN:
				scrn_ctr[SCREEN_CONTROL][1] += NO_PIXELS_TO_MOVE_DRAWING * pixel_eq[SCREEN_CONTROL]
			elif event.key == K_RIGHT:
				scrn_ctr[SCREEN_CONTROL][0] += NO_PIXELS_TO_MOVE_DRAWING * pixel_eq[SCREEN_CONTROL]
			elif event.key == K_q:
				pixel_eq[SCREEN_CONTROL] /= 2
			elif event.key == K_w:
				pixel_eq[SCREEN_CONTROL] *= 2
			elif event.key == K_a:
				SIMULATION_SPEED *= 2
			elif event.key == K_s:
				if SIMULATION_SPEED != 0:
					SIMULATION_SPEED_BEFORE_PAUSE = SIMULATION_SPEED
					SIMULATION_SPEED = 0
				else:
					SIMULATION_SPEED = SIMULATION_SPEED_BEFORE_PAUSE
			elif event.key == K_d:
				SIMULATION_SPEED /= 2
			elif event.key == K_z:
				scrn_ctr[int(not SCREEN_CONTROL)] = scrn_ctr[SCREEN_CONTROL][:]
				pixel_eq[int(not SCREEN_CONTROL)] = pixel_eq[SCREEN_CONTROL]
				SCREEN_CONTROL = 0
				DUAL_SCREEN = not DUAL_SCREEN
			elif event.key == K_e:
				if DUAL_SCREEN == True:
					SCREEN_CONTROL = int(not SCREEN_CONTROL)
	for i in range(UDTs_PER_FRAME):
		universal_delta_time(SIMULATION_SPEED / (UDTs_PER_FRAME * FPS))
	if DUAL_SCREEN == False:
		screen_0 = create_surface_with_all(surf_dims=(WIN_W, WIN_H), pixel_eq=pixel_eq[0], scrn_center = scrn_ctr[0])
		DISPLAYSURF.blit(screen_0, (0, 0))
	else:
		screen_0 = create_surface_with_all(surf_dims=(WIN_W // 2, WIN_H), pixel_eq=pixel_eq[0], scrn_center=scrn_ctr[0], bounding_rect_color=bounding_rect_color[0])
		screen_1 = create_surface_with_all(surf_dims=(WIN_W - WIN_W // 2, WIN_H), pixel_eq=pixel_eq[1], scrn_center = scrn_ctr[1], bounding_rect_color=bounding_rect_color[1])
		DISPLAYSURF.blit(screen_0, (0, 0))
		DISPLAYSURF.blit(screen_1, (WIN_W // 2, 0)) 
	pygame.display.update()
	fpsClock.tick(FPS)

