# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

import sys

import pygame
from pygame.locals import *

from Paddle import Paddle
from BrickCreator import BrickCreator
from Brick import Brick
from Ball import Ball
from CONSTANTS import *

class GameSpace:
	def main(self):
		# 1 -- initialization
		pygame.init()
		self.size = SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("3D Pong Breaker")
		self.clock = pygame.time.Clock()

		# 2 -- create game objects
		# create background surface with black color
		# blit green rectangle (function of hall_length) onto background surface
		# blit hallway corners onto hallway surface
		self.paddle_1 = Paddle(PADDLE_BUFFER, self)
		self.paddle_2 = Paddle(HALLWAY_DEPTH - PADDLE_BUFFER, self)
		self.bc = BrickCreator(self)
		self.bricks = self.bc.get_bricks(BRICK_POS_FN)
		# THIS IS A HACK
		self.ball = Ball(self.paddle_1.rect.center, self.paddle_1.z_pos + 5, BALL_INIT_SPEED, self)

		# 3 -- game loop
		while True:
			# 4 -- clock tick regulation (framerate)
			self.clock.tick(FRAMERATE)

			# 5 -- handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == KEYDOWN:
#					if event.key == K_LEFT:
#						self.paddle_1.is_moving_left = True
#					elif event.key == K_RIGHT:
#						self.paddle_1.is_moving_right = True
#					elif event.key == K_UP:
#						self.paddle_1.is_moving_up = True
#					elif event.key == K_DOWN:
#						self.paddle_1.is_moving_down = True
					# THIS IS A HACK
					if event.key == K_a:
						self.paddle_2.is_moving_left = True
					elif event.key == K_d:
						self.paddle_2.is_moving_right = True
					elif event.key == K_w:
						self.paddle_2.is_moving_up = True
					elif event.key == K_s:
						self.paddle_2.is_moving_down = True
				elif event.type == KEYUP:
#					if event.key == K_LEFT:
#						self.paddle_1.is_moving_left = False
#					elif event.key == K_RIGHT:
#						self.paddle_1.is_moving_right = False
#					elif event.key == K_UP:
#						self.paddle_1.is_moving_up = False
#					elif event.key == K_DOWN:
#						self.paddle_1.is_moving_down = False
					# THIS IS A HACK
					if event.key == K_a:
						self.paddle_2.is_moving_left = False
					elif event.key == K_d:
						self.paddle_2.is_moving_right = False
					elif event.key == K_w:
						self.paddle_2.is_moving_up = False
					elif event.key == K_s:
						self.paddle_2.is_moving_down = False

			# 6 -- tick game objects
			self.paddle_1.tick()
			self.paddle_2.tick()
			self.ball.tick()

			# 7 -- display game objects
			self.screen.fill(COLOR_BLACK)

			# Display hallway outline
			pygame.draw.aaline(self.screen, COLOR_GREEN, (0, 0), WALL_TOP_LEFT)
			pygame.draw.aaline(self.screen, COLOR_GREEN, (SCREEN_WIDTH, 0), WALL_TOP_RIGHT)
			pygame.draw.aaline(self.screen, COLOR_GREEN, (0, SCREEN_HEIGHT), WALL_BOTTOM_LEFT)
			pygame.draw.aaline(self.screen, COLOR_GREEN, (SCREEN_WIDTH, SCREEN_HEIGHT), WALL_BOTTOM_RIGHT)

			pygame.draw.aaline(self.screen, COLOR_GREEN, WALL_OUTLINE_TR, WALL_OUTLINE_TL)
			pygame.draw.aaline(self.screen, COLOR_GREEN, WALL_OUTLINE_TR, WALL_OUTLINE_BR)
			pygame.draw.aaline(self.screen, COLOR_GREEN, WALL_OUTLINE_BL, WALL_OUTLINE_BR)
			pygame.draw.aaline(self.screen, COLOR_GREEN, WALL_OUTLINE_TL, WALL_OUTLINE_BL)

			all_sprites = [self.paddle_1, self.paddle_2, self.ball]
			all_sprites.extend(self.bricks)
			all_sprites.sort(key=lambda sprite: sprite.z_pos, reverse=True)
			
			for sprite in all_sprites:
				self.blit_3D(sprite.image, sprite.rect, sprite.z_pos)
			pygame.display.flip()

	def blit_3D(self, orig_image, orig_rect, z_pos):
		#scale = float(SCALING_FACTOR) / z_pos
		scale = pow(SCALING_FACTOR, z_pos)

		# resize image
		scaled_image_width = orig_image.get_size()[0] * scale
		scaled_image_height = orig_image.get_size()[1] * scale
		scaled_image = pygame.transform.scale(orig_image, (int(scaled_image_width), int(scaled_image_height)))

		# realign center of rectangle
		rect_screen_diff_x = orig_rect.centerx - SCREEN_CENTER_X
		rect_screen_diff_y = orig_rect.centery - SCREEN_CENTER_Y
		scaled_rect = scaled_image.get_rect()
		scaled_rect.centerx = SCREEN_CENTER_X + (rect_screen_diff_x * scale)
		scaled_rect.centery = SCREEN_CENTER_Y + (rect_screen_diff_y * scale)		

		self.screen.blit(scaled_image, scaled_rect)
