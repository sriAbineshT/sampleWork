import pygame,sys
from pygame.locals import *

pygame.init()

SCRWIDTH,SCRHEIGHT=(500,500)
TILEDIM=10 #tells the no of pixels that make one side of a tile 
assert SCRWIDTH%TILEDIM==0 and SCRHEIGHT%TILEDIM==0,"SCRWIDTH and SCRHEIGHT not compatible with TILEDIM"
WHITE=( 255, 255, 255)
BLACK=(   0,   0,   0)
FPS=30
SNAKECOLOR=BLACK
BGCOLOR=WHITE
assert not SNAKECOLOR==BGCOLOR,"Object color same as background"

DISPLAYSURF=pygame.display.set_mode((SCRWIDTH,SCRHEIGHT))
pygame.display.set_caption('SNAKE')

fpsClock=pygame.time.Clock()

def color_tile(pos,color):#draws a tile on the disp surf given pos and given color 
	posx,posy=pos
	pygame.draw.rect(DISPLAYSURF,color,(posx*TILEDIM,posy*TILEDIM,TILEDIM,TILEDIM))

snake_body=[(5,5),(6,5),(7,5),(7,6),(8,6),(9,6),(9,7)]#begins with tail ends in head

def move_snake(dir):#dir is based on keypress event not: 0,0 for no key
	dirx,diry=dir
	headx,heady=snake_body[-1]
	neckx,necky=snake_body[-2]
	nextx,nexty=headx+dirx,heady+diry
	if (dirx,diry)==(0,0) or (nextx,nexty)==(neckx,necky):
		nextx,nexty=2*headx-neckx,2*heady-necky
	del snake_body[0]
	snake_body.append((nextx,nexty))
		
def draw_snake_body(color):
	for part_loc in snake_body:
		color_tile(part_loc,color)

def draw_game_scr():
	#background
	DISPLAYSURF.fill(BGCOLOR)
	#draw_snake
	draw_snake_body(SNAKECOLOR)

while True:
	dirinp=(0,0)
	draw_game_scr()
	for event in pygame.event.get():
		if event.type==QUIT:
			pygame.quit()
			sys.exit()
		elif event.type==KEYUP:
			if event.key==K_UP:
				dirinp=(0,-1)
			if event.key==K_DOWN:
				dirinp=(0,1)
			if event.key==K_LEFT:
				dirinp=(-1,0)
			if event.key==K_RIGHT:
				dirinp=(1,0)
	move_snake(dirinp)
	pygame.display.update()
	fpsClock.tick(FPS)

