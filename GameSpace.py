# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS
# Create set of balls with smart launching
# Make speeds relative to time, not frames

import sys

import pygame
from pygame.locals import *

from Paddle import Paddle
from BrickCreator import BrickCreator
from Brick import Brick
from Ball import Ball
from CONSTANTS import *

class GameSpace:
	def main(self):
		# 1 -- initialization
		pygame.init()
		self.size = SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption("3D Pongbreaker")
		self.clock = pygame.time.Clock()

		# 2 -- create game objects
		self.background = self.create_background()
		self.paddle_1 = Paddle(PADDLE_BUFFER, self)
		self.paddle_2 = Paddle(HALLWAY_DEPTH - PADDLE_BUFFER, self)
		self.bc = BrickCreator(self)
		self.bricks = self.bc.get_bricks(BRICK_POS_FN)
		# THIS IS A HACK
		self.ball = Ball(self.paddle_1.rect.center, self.paddle_1.z_pos + 5, BALL_INIT_SPEED, self)

		# 3 -- game loop
		while True:
			# 4 -- clock tick regulation (framerate)
			self.clock.tick(FRAMERATE)

			# 5 -- handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				# insert code to handle ball launching

			# 6 -- tick game objects
			self.paddle_1.tick()
			self.paddle_2.tick()
			self.ball.tick()

			# 7 -- display game objects
			self.screen.blit(self.background, (0, 0))

			all_sprites = [self.paddle_1, self.paddle_2, self.ball]
			all_sprites.extend(self.bricks)
			all_sprites.sort(key=lambda sprite: sprite.z_pos, reverse=True)

			for sprite in all_sprites:
				self.blit_3D(sprite.image, sprite.rect, sprite.z_pos)

			self.display_ball_trace(self.ball)
			pygame.display.flip()

	def create_background(self):
		background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
		# draw wall edges
		pygame.draw.aaline(background, HALLWAY_EDGE_COLOR, (0, 0), WALL_TL)
		pygame.draw.aaline(background, HALLWAY_EDGE_COLOR, (SCREEN_WIDTH, 0), WALL_TR)
		pygame.draw.aaline(background, HALLWAY_EDGE_COLOR, (0, SCREEN_HEIGHT), WALL_BL)
		pygame.draw.aaline(background, HALLWAY_EDGE_COLOR, (SCREEN_WIDTH, SCREEN_HEIGHT), WALL_BR)
		# draw back wall
		back_wall_pl = [WALL_TL, WALL_TR, WALL_BR, WALL_BL]
		pygame.draw.polygon(background, HALLWAY_EDGE_COLOR, back_wall_pl, HALLWAY_EDGE_THICK)

		return background

	def blit_3D(self, orig_image, orig_rect, z_pos):
		#scale = float(SCALING_FACTOR) / z_pos
		scale = pow(SCALING_FACTOR, z_pos)

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

	def display_ball_trace(self, ball):
		trace_width = SCREEN_WIDTH * pow(SCALING_FACTOR, ball.z_pos)
		trace_height = SCREEN_HEIGHT * pow(SCALING_FACTOR, ball.z_pos)

		trace_tl = (((SCREEN_WIDTH - trace_width) / 2), ((SCREEN_HEIGHT - trace_height) / 2))
		trace_tr = (((SCREEN_WIDTH - trace_width) / 2 + trace_width), ((SCREEN_HEIGHT - trace_height) / 2))
		trace_bl = (((SCREEN_WIDTH - trace_width) / 2), ((SCREEN_HEIGHT - trace_height) / 2 + trace_height))
		trace_br = (((SCREEN_WIDTH - trace_width) / 2 + trace_width), ((SCREEN_HEIGHT - trace_height) / 2 + trace_height))

		trace_pl = [trace_tl, trace_tr, trace_br, trace_bl]

		pygame.draw.polygon(self.screen, HALLWAY_EDGE_COLOR, trace_pl, HALLWAY_EDGE_THICK)
