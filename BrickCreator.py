# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# IMPROVEMENTS
# Have number of brick rows and columns be determined by brick position file

import string
import re
import sys

from Brick import Brick
from CONSTANTS import BRICK_COLORS
from CONSTANTS import N_BRICK_COLUMNS
from CONSTANTS import N_BRICK_ROWS
from CONSTANTS import BRICK_WIDTH
from CONSTANTS import BRICK_HEIGHT
from CONSTANTS import BRICK_PLANE

class BrickCreator:
	def __init__(self, gs=None):
		self.gs = gs
		self.brick_line_RESTR = '(' + "|".join(BRICK_COLORS) + '| ){' + str(N_BRICK_COLUMNS) + '}'
		self.brick_pos_file_RE = re.compile('^' + self.brick_line_RESTR + "(\n" + self.brick_line_RESTR + '){' + str(N_BRICK_ROWS - 1) + '}$')

	def get_bricks(self, brick_pos_fn):
		if not self.verify_brickfile(brick_pos_fn):
			sys.exit('BrickCreator: brick position file incorrectly formatted')

		bricks = set()
		brick_UL_x_poses = [BRICK_WIDTH * number for number in range(N_BRICK_COLUMNS)]
		brick_UL_y_poses = [BRICK_HEIGHT * number for number in range(N_BRICK_ROWS)]

		with open(brick_pos_fn, 'r') as brick_pos_f:
			brick_pos_ls = brick_pos_f.readlines()
			for row in range(N_BRICK_ROWS):
				for col in range(N_BRICK_COLUMNS):
					if brick_pos_ls[row][col] != ' ':
						bricks.add(Brick(brick_pos_ls[row][col], (brick_UL_x_poses[col], brick_UL_y_poses[row]), 'topleft', BRICK_PLANE, self.gs))
		return bricks

	def verify_brickfile(self, brick_pos_fn):
		with open(brick_pos_fn, 'r') as brick_pos_f:
			return self.brick_pos_file_RE.match(brick_pos_f.read())
