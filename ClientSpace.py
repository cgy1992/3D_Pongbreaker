# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

import pygame
from pygame.locals import *

from Paddle import Paddle
from Brick import Brick
from Ball import Ball
from CONSTANTS import *

class ClientSpace:
	def __init__(self):
		# 1 -- initialization
		pygame.init()
		self.size = SCREEN_WIDTH, SCREEN_HEIGHT
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption('3D Pongbreaker Client')

		# 2 -- create static game objects
		self.background = self.create_background()
		self.paddle_2 = Paddle(PADDLE_BUFFER, self)
		self.paddle_1 = Paddle(HALLWAY_DEPTH - PADDLE_BUFFER, self)
		self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
		self.paddle_1_title_text = self.title_font.render('Player 1', False, TEXT_COLOR)
		self.paddle_2_title_text = self.title_font.render('Player 2', False, TEXT_COLOR)
		self.paddle_1_title_rect = self.paddle_1_title_text.get_rect()
		self.paddle_2_title_rect = self.paddle_2_title_text.get_rect()
		self.score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

	def update_screen(self, pos_dict):
		self.paddle_2.rect.center = pos_dict['p2']
		self.paddle_1.rect.center = pos_dict['p1']
		for ball_pos in pos_dict['balls']:
			

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
