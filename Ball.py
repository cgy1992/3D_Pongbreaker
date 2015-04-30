# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

import pygame

from CONSTANTS import *
class Ball(pygame.sprite.Sprite):
	def __init__(self, z_pos, gs):
		# initialize
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.Surface([(BALL_RADIUS * 2), (BALL_RADIUS * 2)])
		self.image = pygame.draw.circle(self.image, PADDLE_COLOR, BALL_RADIUS, BALL_RADIUS)
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN_CENTER_X, SCREEN_CENTER_Y)
		self.z_pos = z_pos

		# properties
		x_vel = 0
		y_vel = 0
		z_vel = 0

	def tick(self):
		# move ball inside bounds if outside
		if self.is_out_left_bound():
			self.rect.left = 0
		elif self.is_out_right_bound():
			self.rect.right = SCREEN_WIDTH
		if self.is_out_top_bound():
			self.rect.top = 0
		elif self.is_out_bottom_bound():
			self.rect.bottom = SCREEN_HEIGHT
		# reverse x or y direction if ball is touching bounds
		if self.is_on_left_bound() or self.is_on_right_bound():
			self.x_vel *= -1
		if self.is_on_top_bound() or self.is_on_bottom_bound():
			self.y_vel *= -1
		# reverse z direction if ball is touching paddle
		if self.rect.colliderect(gs.

	def colliderect_3D(rect1, rect2, z_pos1, z_pos2):
		return z_pos1 == z_pos2 and rect1.colliderect(rect2)		

	def is_on_left_bound(self):
		return self.rect.left = 0

	def is_on_right_bound(self):
		return self.rect.right = SCREEN_WIDTH

	def is_on_top_bound(self):
		return self.rect.top = 0

	def is_on_bottom_bound(self):
		return self.rect.bottom = SCREEN_HEIGHT

	def is_out_left_bound(self):
		return self.rect.left < 0

	def is_out_right_bound(self):
		return self.rect.right > SCREEN_WIDTH

	def is_out_top_bound(self):
		return self.rect.top < 0

	def is_out_bottom_bound(self):
		return self.rect.bottom > SCREEN_HEIGHT	
