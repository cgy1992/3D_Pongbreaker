# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

import time

import pygame
from pygame.locals import *

from BrickCreator import BrickCreator
from Brick import Brick
from CONSTANTS import *

class GameSpace:
	def main(self):
		# 1 -- initialization
		pygame.init()
		self.size = SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen = pygame.display.set_mode(self.size)
		self.clock = pygame.time.Clock()

		# 2 -- create game objects
		# create background surface with black color
		# blit green rectangle (function of hall_length) onto background surface
		# blit hallway corners onto hallway surface
		self.bc = BrickCreator(self)
		self.bricks = self.bc.get_bricks(BRICK_POS_FN)

		# 3 -- game loop
		while True:
			# 4 -- clock tick regulation (framerate)
			self.clock.tick(FRAMERATE)

			# 5 -- handle user inputs

			# 6 -- tick game objects

			# 7 -- display game objects
			self.screen.fill(COLOR_BLACK)
			for brick in self.bricks:
				self.blit_3D(brick.image, brick.rect, brick.z)
			pygame.display.flip()

	def blit_3D(self, orig_image, orig_rect, z_pos):
		scale = float(SCREEN_FACTOR) / z_pos

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
