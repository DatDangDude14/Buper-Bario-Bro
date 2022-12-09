import pygame
from tiles import Tile
from tiles import Flag
from settings import tile_size, screen_width
from player import Player
from enemy import Enemy

class Level:
	def __init__(self,level_data,surface):

		# level setup
		self.display_surface = surface
		self.setup_level(level_data)
		self.world_shift = 0
		self.current_x = 0
		self.running = 'title'

	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()
		self.flag = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.enemy = pygame.sprite.Group()

		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if cell == 'X':
					tile = Tile((x,y),tile_size)
					self.tiles.add(tile)
				if cell == 'P':
					player = Player((x,y))
					self.player.add(player)
				if cell == 'G':
					goomba = Enemy((x,y), 'goomba')
					self.enemy.add(goomba)
				if cell == 'F':
					flag = Flag((x+10,y+69),'F')
					self.flag.add(flag)
				if cell == 'F':
					red = Flag((x-120,y-440),'R')
					self.flag.add(red)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for flag in self.flag.sprites():
			if flag.rect.colliderect(player.rect):
				self.running = 'winning'

		for enemy in self.enemy.sprites():
			for sprite in self.tiles.sprites():
				if sprite.rect.colliderect(enemy.rect):
					if enemy.direction.x < 0:
						enemy.rect.left = sprite.rect.right
						enemy.move_speed = 3
					elif enemy.direction.x > 0:
						enemy.rect.right = sprite.rect.left
						enemy.move_speed = -3


		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.left > self.current_x or player.direction.x <= 0):
			player.on_right = False


	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for enemy in self.enemy.sprites():
			enemy.apply_gravity()
			if enemy.rect.colliderect(player.rect):
					if player.direction.y > 1.7:
						player.jump()
						enemy.status = 'dead'
						enemy.kill()
					else:
						self.running = 'dead'
			for sprite in self.tiles.sprites():
				if sprite.rect.colliderect(enemy.rect):
					if enemy.direction.y > 0:
						enemy.rect.bottom = sprite.rect.top
						enemy.direction.y = 0
					elif enemy.direction.y < 0:
						enemy.rect.top = sprite.rect.bottom
						enemy.direction.y = 0

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.rect.y > 704:
			self.running = 'dead'

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0:
			player.on_ceiling = False


	def run(self):

		# level tiles
		self.flag.update(self.world_shift)
		self.flag.draw(self.display_surface)

		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)
		self.scroll_x()

		# player
		self.player.update()
		self.horizontal_movement_collision()
		self.vertical_movement_collision()
		self.player.draw(self.display_surface)

		#enemy tiles
		self.enemy.update(self.world_shift)
		self.enemy.draw(self.display_surface)