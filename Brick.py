# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

import pygame

from CONSTANTS import *

class Brick(pygame.sprite.Sprite):
	def __init__(self, color, topleft, z_pos, gs):
		# initialize
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
		self.image.fill(BRICK_COLORS[color])
		self.rect = self.image.get_rect()
		self.rect.topleft = topleft
		self.z_pos = z_pos
