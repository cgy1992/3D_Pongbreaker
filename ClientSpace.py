# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# IMPROVEMENTS
# Make make tuples more clear in Pickle (dicts?)
# Make traces transparent

import sys

import pygame
from pygame.locals import QUIT
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEBUTTONUP

from Paddle import Paddle
from Brick import Brick
from Ball import Ball

from CONSTANTS import SCREEN_WIDTH
from CONSTANTS import SCREEN_HEIGHT
from CONSTANTS import PADDLE_BUFFER
from CONSTANTS import HALLWAY_DEPTH
from CONSTANTS import TITLE_FONT_SIZE
from CONSTANTS import TEXT_COLOR
from CONSTANTS import SCORE_FONT_SIZE
from CONSTANTS import SCREEN_CENTER_X
from CONSTANTS import SCREEN_CENTER_Y
from CONSTANTS import HALLWAY_CENTER
from CONSTANTS import WALL_TL
from CONSTANTS import WALL_TR
from CONSTANTS import WALL_BL
from CONSTANTS import WALL_BR
from CONSTANTS import HALLWAY_EDGE_COLOR
from CONSTANTS import HALLWAY_EDGE_THICK
from CONSTANTS import SCALING_FACTOR

class ClientSpace:
	def __init__(self):
		# initialization
		pygame.init()
		self.size = SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('3D Pongbreaker Client')

		# create static game objects
		self.background = self.create_background()
		self.paddle_1 = Paddle((HALLWAY_DEPTH - PADDLE_BUFFER), 'not used', self)
		self.paddle_2 = Paddle(PADDLE_BUFFER, 'not used', self)
		self.bricks = set()
		self.balls = set()
		self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
		self.paddle_1_title_text = self.title_font.render('Player 1', False, TEXT_COLOR)
		self.paddle_2_title_text = self.title_font.render('Player 2', False, TEXT_COLOR)
		self.paddle_1_title_rect = self.paddle_1_title_text.get_rect()
		self.paddle_2_title_rect = self.paddle_2_title_text.get_rect()
		self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

	def update_screen(self, pos_dict):
		# handle exit user input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				self.paddle_2.launch = True
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				self.paddle_2.launch = False

		# update position of paddles
		self.paddle_1.rect.center = ((self.rev_x(pos_dict['p1'][0][0]), pos_dict['p1'][0][1]))
		self.paddle_2.rect.center = ((self.rev_x(pos_dict['p2'][0][0]), pos_dict['p2'][0][1]))
		# update paddle scores
		self.paddle_1.score = pos_dict['p1'][1]
		self.paddle_2.score = pos_dict['p2'][1]
		# reset and fill position of brick(s)
		self.bricks = set()
		for brick_pos in pos_dict['bricks']:
			self.bricks.add(Brick(brick_pos[2], (self.rev_x(brick_pos[0][0]), brick_pos[0][1]), 'center', self.rev_z(brick_pos[1]), self))
		# reset and fill position of ball(s)
		self.balls = set()
		for ball_pos in pos_dict['balls']:
			color = ball_pos[2]
			self.balls.add(Ball((self.rev_x(ball_pos[0][0]), ball_pos[0][1]), self.rev_z(ball_pos[1]), 'not used', self, ball_pos[2]))

		# display background
		self.screen.blit(self.background, (0, 0))

		# display sprites
		sprites = [self.paddle_1, self.paddle_2]
		sprites.extend(self.bricks)
		sprites.extend(self.balls)
		sprites.sort(key=lambda sprite: sprite.z_pos, reverse=True)
		for sprite in sprites:
			self.blit_3D(sprite)

		# display ball traces
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

	def rev_x(self, x):
		diff = x - SCREEN_CENTER_X
		return SCREEN_CENTER_X - diff

	def rev_z(self, z):
		diff = z - HALLWAY_CENTER
		return HALLWAY_CENTER - diff

	def get_mouse(self):
		(mx, my) = pygame.mouse.get_pos()
		return (self.rev_x(mx), my)

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
