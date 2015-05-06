# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS
# Make velocity a function of last 0.5? seconds

import pygame

from CONSTANTS import PADDLE_WIDTH
from CONSTANTS import PADDLE_HEIGHT
from CONSTANTS import PADDLE_COLOR
from CONSTANTS import PADDLE_ALPHA
from CONSTANTS import SCREEN_CENTER_X
from CONSTANTS import SCREEN_CENTER_Y

class Paddle(pygame.sprite.Sprite):
	def __init__(self, z_pos, owner, gs):
		# initialize
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
		self.image.fill(PADDLE_COLOR)
		self.image.set_alpha(PADDLE_ALPHA)
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN_CENTER_X, SCREEN_CENTER_Y)
		self.z_pos = z_pos
		self.old_x_pos = int()
		self.old_y_pos = int()
		self.manual_x = 400
		self.manual_y = 400
		self.owner = owner # {host, client}
		self.launch = False
		self.score = 0

	def tick(self):
		self.old_x_pos = self.rect.centerx
		self.old_y_pos = self.rect.centery
		if self.owner == 'host':
			self.rect.center = pygame.mouse.get_pos()
		else:
			self.rect.center = (self.manual_x, self.manual_y)

	def get_vel(self):
		return ((self.rect.centerx - self.old_x_pos), (self.rect.centery - self.old_y_pos))
