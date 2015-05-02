# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS
# Better ball launching (quick mouse clicks not detected)

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
		self.balls = set()
		self.balls.add(Ball(1, self))
		self.balls.add(Ball(2, self))
		self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
		self.paddle_1_title_text = self.title_font.render('Player 1', False, TEXT_COLOR)
		self.paddle_2_title_text = self.title_font.render('Player 2', False, TEXT_COLOR)
		self.paddle_1_title_rect = self.paddle_1_title_text.get_rect()
		self.paddle_2_title_rect = self.paddle_2_title_text.get_rect()
		self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

	# 3 -- game loop
	def GameLoop(self):
		# 4 -- clock tick regulation (framerate)
		#self.clock.tick(FRAMERATE)

		# 5 -- handle user inputs
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				self.paddle_1.launch = True
				self.paddle_2.launch = True
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				self.paddle_1.launch = False
				self.paddle_2.launch = False

		# 6 -- tick/update game objects
		self.paddle_1.tick()
		self.paddle_2.tick()
		for ball in set(self.balls):
			ball.tick()

		# 7 -- display game objects
		self.screen.blit(self.background, (0, 0))

		sprites = [self.paddle_1, self.paddle_2]
		sprites.extend(self.bricks)
		sprites.extend(self.balls)
		sprites.sort(key=lambda sprite: sprite.z_pos, reverse=True)
		for sprite in sprites:
			self.blit_3D(sprite)

		for ball in self.balls:
			self.display_ball_trace(ball)

		# create score texts and rects
		paddle_1_score_text = self.score_font.render(str(self.paddle_1.score), False, TEXT_COLOR)
		paddle_2_score_text = self.score_font.render(str(self.paddle_2.score), False, TEXT_COLOR)
		paddle_1_score_rect = paddle_1_score_text.get_rect()
		paddle_2_score_rect = paddle_2_score_text.get_rect()
		# align title and score rects
		paddle_1_score_rect.bottomleft = (0, SCREEN_HEIGHT)
		paddle_2_score_rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
		self.paddle_1_title_rect.bottomleft = paddle_1_score_rect.topleft
		self.paddle_2_title_rect.bottomright = paddle_2_score_rect.topright
		# blit titles and scores
		self.screen.blit(self.paddle_1_title_text, self.paddle_1_title_rect)
		self.screen.blit(self.paddle_2_title_text, self.paddle_2_title_rect)
		self.screen.blit(paddle_1_score_text, paddle_1_score_rect)
		self.screen.blit(paddle_2_score_text, paddle_2_score_rect)

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

	def blit_3D(self, sprite):
		scale = pow(SCALING_FACTOR, sprite.z_pos)
		# resize image
		scaled_image_width = sprite.image.get_size()[0] * scale
		scaled_image_height = sprite.image.get_size()[1] * scale
		scaled_image = pygame.transform.scale(sprite.image, (int(scaled_image_width), int(scaled_image_height)))
		# realign center of rectangle
		rect_screen_diff_x = sprite.rect.centerx - SCREEN_CENTER_X
		rect_screen_diff_y = sprite.rect.centery - SCREEN_CENTER_Y
		scaled_rect = scaled_image.get_rect()
		scaled_rect.centerx = SCREEN_CENTER_X + (rect_screen_diff_x * scale)
		scaled_rect.centery = SCREEN_CENTER_Y + (rect_screen_diff_y * scale)

		self.screen.blit(scaled_image, scaled_rect)

	def display_ball_trace(self, ball):
		# calculate trace dimensions
		trace_width = SCREEN_WIDTH * pow(SCALING_FACTOR, ball.z_pos)
		trace_height = SCREEN_HEIGHT * pow(SCALING_FACTOR, ball.z_pos)
		# calculate trace corners
		trace_tl = (((SCREEN_WIDTH - trace_width) / 2), ((SCREEN_HEIGHT - trace_height) / 2))
		trace_tr = (((SCREEN_WIDTH - trace_width) / 2 + trace_width), ((SCREEN_HEIGHT - trace_height) / 2))
		trace_bl = (((SCREEN_WIDTH - trace_width) / 2), ((SCREEN_HEIGHT - trace_height) / 2 + trace_height))
		trace_br = (((SCREEN_WIDTH - trace_width) / 2 + trace_width), ((SCREEN_HEIGHT - trace_height) / 2 + trace_height))
		# draw trace
		trace_pl = [trace_tl, trace_tr, trace_br, trace_bl]
		pygame.draw.polygon(self.screen, HALLWAY_EDGE_COLOR, trace_pl, HALLWAY_EDGE_THICK)
