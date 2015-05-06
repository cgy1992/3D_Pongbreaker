# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS
# Decide on initial x and y velocity
# Make an actual circle
# Better paddle velocity transferral
# Revisit collisions
# Collision sounds
# Collision flash?
# Client ball launching?

import pygame

from CONSTANTS import *

class Ball(pygame.sprite.Sprite):
	def __init__(self, center, z_pos, last_hit, gs, color_overide=None):
		# initialize
		pygame.sprite.Sprite.__init__(self)
		self.gs = gs
		self.image = pygame.Surface(((BALL_RADIUS * 2), (BALL_RADIUS * 2)))
		if color_overide:		# used for client player
			self.color = color_overide
			self.image.fill(self.color)
		else:
			self.color = BALL_COLOR	
			self.image.fill(self.color)	
		self.rect = self.image.get_rect()
		self.last_hit = last_hit
		self.rect.center = center
		self.z_pos = z_pos
		self.state = 'on paddle' # {on paddle, launch, in play, out}
		self.x_vel = 0
		self.y_vel = 0
		self.z_vel = 0
		self.out_on = int()
		self.n_on_paddle_frames = 0
		self.n_out_frames = 0

	def tick(self):
		if self.state == 'on paddle':
			# move ball with paddle
			if self.last_hit == 1:
				self.rect.center = self.gs.paddle_1.rect.center
			elif self.last_hit == 2:
				self.rect.center = self.gs.paddle_2.rect.center
			# increment number of on paddle frames
			self.n_on_paddle_frames += 1
			# make ball in play if hosting paddle is launching or if time expires
			if self.last_hit == 1 and self.gs.paddle_1.launch:
				self.state = 'launch'
			elif self.last_hit == 2 and self.gs.paddle_2.launch:
				self.state = 'launch'
			elif self.n_on_paddle_frames > MAX_ON_PADDLE_FRAMES:
				self.state = 'launch'
		elif self.state == 'launch':
			# Play launch sound
			pygame.mixer.music.load("./sounds/blip.wav")
			pygame.mixer.music.play()

			# set initial x-, y-, and z-velocity
			self.x_vel = 0.5 * BALL_INIT_VEL
			self.y_vel = 0.75 * BALL_INIT_VEL
			if self.last_hit == 1:
				self.z_vel = BALL_INIT_VEL
			elif self.last_hit == 2:
				self.z_vel = -BALL_INIT_VEL
			self.state = 'in play'
		elif self.state == 'in play':
			self.color = BALL_COLOR
			self.image.fill(self.color)
			# regenerate and update score if ball leaves hallway on player 1 side
			if self.z_pos < 0:
				self.gs.paddle_2.score += SCORE_VAL
				self.out_on = 1
				self.state = 'out'
				return
			# adjust score and regenerate if ball leaves hallway on player 2 side
			elif self.z_pos > HALLWAY_DEPTH:
				self.gs.paddle_1.score += SCORE_VAL
				self.out_on = 2
				self.state = 'out'
				return
			# reverse x- or y-direction if ball is touching bounds (or will touch) walls
			if self.is_out_left_bound(self.rect.move(self.x_vel, 0)) or self.is_out_right_bound(self.rect.move(self.x_vel, 0)):
				self.x_vel *= -1
			if self.is_out_top_bound(self.rect.move(0, self.y_vel)) or self.is_out_bottom_bound(self.rect.move(0, self.y_vel)):
				self.y_vel *= -1
			# reverse z-direction, adjust x- and y- velocity, and update last hit if ball is touching (or will touch) either paddle
			if self.colliderect_3D(self.gs.paddle_1):
				self.color = BALL_COLLIDE_COLOR
				self.image.fill(self.color)
				# reverse z-direction
				self.z_vel *= -1
				# add partial velocity of paddle
				paddle_vel = self.gs.paddle_1.get_vel()
				self.x_vel = paddle_vel[0] * PADDLE_TRANSFER_FRAC
				self.y_vel = paddle_vel[1] * PADDLE_TRANSFER_FRAC
				# update last hit
				self.last_hit = 1
			elif self.colliderect_3D(self.gs.paddle_2):
				self.color = BALL_COLLIDE_COLOR
				self.image.fill(self.color)
				# reverse z-direction
				self.z_vel *= -1
				# add partial velocity of paddle
				paddle_vel = self.gs.paddle_2.get_vel()
				self.x_vel = paddle_vel[0] * PADDLE_TRANSFER_FRAC
				self.y_vel = paddle_vel[1] * PADDLE_TRANSFER_FRAC
				# update last hit
				self.last_hit = 2
			# reverse z-direction, delete brick, and adjust score if ball is touching (or will touch) any brick
			for brick in set(self.gs.bricks):
				if self.colliderect_3D(brick):
					self.color = BALL_COLLIDE_COLOR
					self.image.fill(self.color)
					self.z_vel *= -1
					self.gs.bricks.remove(brick)
					if self.last_hit == 1:
						self.gs.paddle_1.score += BRICK_VAL
					elif self.last_hit == 2:
						self.gs.paddle_2.score += BRICK_VAL
			# move ball
			self.rect.move_ip(self.x_vel, self.y_vel)
			self.z_pos += self.z_vel
		elif self.state == 'out':
			self.color = BALL_OUT_COLOR
			self.image.fill(self.color)
			self.n_out_frames += 1
			if self.n_out_frames > OUT_FRAMES:
				if self.out_on == 1:
					self.gs.balls.add(Ball(self.gs.paddle_2.rect.center, (self.gs.paddle_2.z_pos - 1), 2, self.gs))
				elif self.out_on == 2:
					self.gs.balls.add(Ball(self.gs.paddle_1.rect.center, (self.gs.paddle_1.z_pos + 1), 1, self.gs))
				self.gs.balls.remove(self)

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
