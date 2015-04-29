# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker

### THIS IS NOT A PRODUCTION FILE. THIS FILE IS A 'VISION' OF WHAT THE	   ###
### GameSpace CLASS WILL LOOK LIKE										   ###

import pygame
from pygame.locals import *

from CONSTANTS import *

class GameSpace:
	def main(self):
		# 1 -- initialization
		pygame.init()
		self.size = SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen = pygame.display.set_mode(self.size)

		# 2 -- create game objects
		# create background surface with black color
		# blit green rectangle (function of hall_length) onto background surface
		# blit hallway corners onto hallway surface
		self.paddle_2 = Paddle(HALLWAY_DEPTH)
		self.bc = BrickCreator()
		self.bricks = self.bc.get_bricks(BRICKS_POS_FN)
		self.balls = set()
		self.balls.add(Ball(self.paddle_1))
		self.balls.add(Ball(self.paddle_2))
		self.paddle_1 = Paddle(0)

		# 3 -- game loop
		while True:
			# 4 -- clock tick regulation (framerate)
			self.clock.tick(self.FRAMERATE)

			# 5 -- handle user inputs
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit(0)
				elif event.type == KEYDOWN:
					if event.key == K_LEFT:
						self.paddle_1.is_moving_left = True
					elif event.key == K_RIGHT:
						self.paddle_1.is_moving_right = True
					elif event.key == K_UP:
						self.paddle_1.is_moving_up = True
					elif event.key == K_DOWN:
						self.paddle_1.is_moving_down = True
					elif event.key == K_a:
						self.paddle_2.is_moving_left = True
					elif event.key == K_d:
						self.paddle_2.is_moving_right = True
					elif event.key == K_w:
						self.paddle_2.is_moving_up = True
					elif event.key == K_s:
						self.paddle_2.is_moving_down = True
				elif event.type == KEYUP:
					if event.key == K_LEFT:
						self.paddle_1.is_moving_left = False
					elif event.key == K_RIGHT:
						self.paddle_1.is_moving_right = False
					elif event.key == K_UP:
						self.paddle_1.is_moving_up = False
					elif event.key == K_DOWN:
						self.paddle_1.is_moving_down = False
					elif event.key == K_a:
						self.paddle_2.is_moving_left = False
					elif event.key == K_d:
						self.paddle_2.is_moving_right = False
					elif event.key == K_w:
						self.paddle_2.is_moving_up = False
					elif event.key == K_s:
						self.paddle_2.is_moving_down = False

			# 6 -- tick game objects
			self.paddle_1.tick()
			self.paddle_2.tick()
			for ball in self.balls:
				ball.tick()

			# 7 -- display game objects
			# blit assembled background
			self.screen.blit(self.player_2.image, self.player_2.rect)
			for brick in self.bricks:
				self.screen.blit(brick.image, brick.rect)
			for ball in self.balls:
				self.screen.blit(ball.image, ball.rect)
			self.screen.blit(self.player_1.image, self.player_2.rect)
