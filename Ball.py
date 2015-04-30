# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS
# Decide on initial x and y velocity

import pygame

from CONSTANTS import *

class Ball(pygame.sprite.Sprite):
	def __init__(self, center, z_pos, z_init_vel, gs):
		# initialize
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.Surface([(BALL_RADIUS * 2), (BALL_RADIUS * 2)])
		self.rect = pygame.draw.circle(self.image, BALL_COLOR, center, BALL_RADIUS)
		self.z_pos = z_pos

		# properties
		self.x_vel = 0.25 * z_init_vel
		self.y_vel = 0.6 * z_init_vel
		self.z_vel = z_init_vel

	def tick(self):
		# reverse x or y direction if ball is touching bounds (or will touch) bounds
		if self.is_out_left_bound(self.rect.move(self.x_vel, 0)) or self.is_out_right_bound(self.rect.move(self.x_vel, 0)):
			self.x_vel *= -1
		if self.is_out_top_bound(self.rect.move(0, self.y_vel)) or self.is_out_bottom_bound(self.rect.move(0, self.y_vel)):
			self.y_vel *= -1
		# reverse z direction if ball is touching (or will touch) either paddle
		if self.colliderect_3D(self.gs.paddle_1) or self.colliderect_3D(self.gs.paddle_2):
			self.z_vel *= -1
		# reverse z direction and delete brick if ball is touching (or will touch) any brick
		for brick in list(self.gs.bricks):
			if self.colliderect_3D(brick):
				self.z_vel *= -1
				self.gs.brick.remove(brick)
		# move ball
		self.rect.move_ip(self.x_vel, self.y_vel)
		self.z_pos += self.z_vel

	def colliderect_3D(self, other):
		return ((self.z_pos <= other.z_pos and (self.z_pos + self.z_vel) >= other.z_pos) or (self.z_pos >= other.z_pos and (self.z_pos + self.z_vel) <= other.z_pos)) and self.rect.colliderect(other.rect)		

	def is_out_left_bound(self, rect):
		return rect.left < 0

	def is_out_right_bound(self, rect):
		return rect.right > SCREEN_WIDTH

	def is_out_top_bound(self, rect):
		return rect.top < 0

	def is_out_bottom_bound(self, rect):
		return rect.bottom > SCREEN_HEIGHT	
