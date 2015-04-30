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
		self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
		self.image.fill(PADDLE_COLOR)
		self.image.set_alpha(PADDLE_ALPHA)
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN_CENTER_X, SCREEN_CENTER_Y)
		self.z_pos = z_pos

		# properties
		self.is_moving_left = False
		self.is_moving_right = False
		self.is_moving_up = False
		self.is_moving_down = False

	def tick(self):
		if self.is_moving_left:
				if self.is_out_left_bound(self.rect.move(-PADDLE_SPEED, 0)):
					self.rect.left = 0
				else:
					self.rect.move_ip(-PADDLE_SPEED, 0)
		if self.is_moving_right:
				if self.is_out_right_bound(self.rect.move(PADDLE_SPEED, 0)):
					self.rect.right = SCREEN_WIDTH
				else:
					self.rect.move_ip(PADDLE_SPEED, 0)
		if self.is_moving_up:
				if self.is_out_top_bound(self.rect.move(0, -PADDLE_SPEED)):
					self.rect.top = 0
				else:
					self.rect.move_ip(0, -PADDLE_SPEED)
		if self.is_moving_down:
				if self.is_out_bottom_bound(self.rect.move(0, PADDLE_SPEED)):
					self.rect.bottom = SCREEN_HEIGHT
				else:
					self.rect.move_ip(0, PADDLE_SPEED)

	def is_out_left_bound(self, rect):
		return rect.left < 0

	def is_out_right_bound(self, rect):
		return rect.right > SCREEN_WIDTH

	def is_out_top_bound(self, rect):
		return rect.top < 0

	def is_out_bottom_bound(self, rect):
		return rect.bottom > SCREEN_HEIGHT	  
