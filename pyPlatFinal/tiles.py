import pygame

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size):
		super().__init__()
		self.image = pygame.Surface((size,size))
		block = pygame.image.load("graphics/pixil-frame-0.png")
		self.image = block
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift

class Flag(pygame.sprite.Sprite):
	def __init__(self,pos,size):
		super().__init__()
		if size == 'F':
			self.image = pygame.image.load("graphics/Flag.png").convert()
			self.rect = self.image.get_rect(bottomleft = pos)
		if size == 'R':
			self.image = pygame.image.load("graphics/Red.png").convert()
			self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift):
		self.rect.x += x_shift