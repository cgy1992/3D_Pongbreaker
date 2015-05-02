# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

import pygame

from CONSTANTS import *

class Paddle(pygame.sprite.Sprite):
	def __init__(self, z_pos, gs):
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
		self.launch = False
		self.score = 0

	def tick(self):
		self.old_x_pos = self.rect.centerx
		self.old_y_pos = self.rect.centery
		self.rect.center = pygame.mouse.get_pos()

	def get_vel(self):
		return ((self.rect.centerx - self.old_x_pos), (self.rect.centery - self.old_y_pos))
