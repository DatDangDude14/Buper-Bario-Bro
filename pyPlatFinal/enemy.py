import pygame
from support import import_folder

class Enemy(pygame.sprite.Sprite):
	def __init__(self, pos, type):
		super().__init__()
		self.import_enemy_assets()
		self.frame_index = 0
		self.animation_speed = 0.05
		self.image = self.animations['goomba'][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)

		self.direction = pygame.math.Vector2(0,0)

		self.status = 'goomba'
		self.gravity = 0.8
		self.move_speed = -3
		self.alive = True


	def import_enemy_assets(self):
		character_path = './graphics/enemy/'
		self.animations = {'goomba':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		image = animation[int(self.frame_index)]
		self.image = image

	def move(self):
		self.rect.x += self.move_speed
		if(self.move_speed < 0):
			self.direction.x = -1
		if(self.move_speed > 0):
			self.direction.x = 1

	def shift(self,x_shift):
		self.rect.x += x_shift

	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def update(self, x_shift):
		self.rect.x += x_shift
		self.move()
		self.animate()
		