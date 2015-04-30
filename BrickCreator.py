# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS
# Have number of brick rows and columns be determined by brick position file
# Multiple walls per file

import re
import string
import sys

from Brick import Brick
from CONSTANTS import *

class BrickCreator:
	def __init__(self, gs=None):
		self.gs = gs
		self.brick_line_RE = '(' + "|".join(BRICK_COLORS) + '| ){' + str(N_BRICK_COLUMNS) + '}'
		self.brick_wall_RE = self.brick_line_RE + "(\n" + self.brick_line_RE + '){' + str(N_BRICK_ROWS - 1) + '}'
		self.brick_pos_file_RE = '^' + self.brick_wall_RE + "(\n\n" + self.brick_wall_RE + ')*$'

	def get_bricks(self, brick_pos_fn):
		if not self.verify_brickfile(brick_pos_fn):
			print 'BrickCreator: brick position file incorrectly formatted'
			sys.exit()

		bricks = list()
		brick_UL_x_poses = [BRICK_WIDTH * number for number in xrange(N_BRICK_COLUMNS)]
		brick_UL_y_poses = [BRICK_HEIGHT * number for number in xrange(N_BRICK_ROWS)]

		with open(brick_pos_fn, 'r') as brick_pos_f:
			brick_pos_ls = brick_pos_f.readlines()
			for row in xrange(N_BRICK_ROWS):
				for col in xrange(N_BRICK_COLUMNS):
					if brick_pos_ls[row][col] != ' ':
						bricks.append(Brick(brick_pos_ls[row][col], (brick_UL_x_poses[col], brick_UL_y_poses[row]), BRICK_PLANE, self.gs))
		return bricks

	def verify_brickfile(self, brick_pos_fn):
		with open(brick_pos_fn, 'r') as brick_pos_f:
			return re.match(self.brick_pos_file_RE, brick_pos_f.read())
