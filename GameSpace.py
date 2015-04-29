# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

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
				self.screen.blit(brick.image, brick.rect)
			pygame.display.flip()
