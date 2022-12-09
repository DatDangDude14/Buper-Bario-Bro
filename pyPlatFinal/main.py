import pygame, sys
from settings import *
from tiles import Tile
from level import Level

#Pygame setup
pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
sky_surf = pygame.image.load('graphics/sunset.png').convert()
title_surf = pygame.image.load('graphics/title.png').convert()
title_bar = pygame.image.load("graphics/character/idle/FakeMario.png").convert()
hit2play = pygame.image.load("graphics/hit2play.png").convert()
gameover = pygame.image.load("graphics/gameover.png").convert()
win = pygame.image.load("graphics/dubz.png").convert()
clock = pygame.time.Clock()
level = Level(level_map,screen)

bg_music = pygame.mixer.Sound('audio/guile.mp3')
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and level.running != 'dead' and level.running != 'winning':
				level.running = 'running'

	if(level.running == 'title'):
		screen.fill('gray')
		screen.blit(title_surf, (250,200))
		screen.blit(hit2play, (445,500))
		pygame.display.update()

	elif(level.running == 'running'):
		screen.blit(sky_surf,(0,0))
		level.run()
		pygame.display.update()

	elif(level.running == 'winning'):
		screen.blit(win, (0,0))
		pygame.display.update()

	else:
		screen.blit(gameover,(0,0))
		level.enemy.empty()
		pygame.display.update()

	clock.tick(60)