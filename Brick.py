# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# IMPROVEMENTS
# position first

import pygame

from CONSTANTS import BRICK_WIDTH
from CONSTANTS import BRICK_HEIGHT
from CONSTANTS import BRICK_COLORS
from CONSTANTS import BRICK_ALPHA

class Brick(pygame.sprite.Sprite):
	def __init__(self, color, topleft_or_center, pos_ind, z_pos, gs):
		# initialize
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.color = color
		self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
		self.color = color
		self.image.fill(BRICK_COLORS[color])
		self.image.set_alpha(BRICK_ALPHA)
		self.rect = self.image.get_rect()
		if pos_ind == 'topleft':
			self.rect.topleft = topleft_or_center
		else:
			self.rect.center = topleft_or_center
		self.z_pos = z_pos
