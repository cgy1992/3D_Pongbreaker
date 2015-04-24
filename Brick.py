import pygame
from GameSpace import GameSpace

from CONSTANTS import *


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, topleft, gs=None):
        # initialize
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(BRICK_COLOR[color])
        self.rect = self.image.get_rect
        self.rect.topleft = topleft
