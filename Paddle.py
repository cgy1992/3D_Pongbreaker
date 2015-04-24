import pygame
from GameSpace import GameSpace

from CONSTANTS import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, gs=None):
        # initialize
        pygame.sprite.Sprite.__init__(self)
        self.gs = gs
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect

        # properties
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_moving_up = False
        self.is_moving_down = False

    def tick():
        if self.is_moving_left and not self.is_out_left_bound():
            self.rect.move_ip(-PADDLE_SPEED, 0)
        if self.is_moving_right and not self.is_out_right_bound():
            self.rect.move_ip(PADDLE_SPEED, 0)
        if self.is_moving_up and not self.is_out_top_bound():
            self.rect.move_ip(0, -PADDLE_SPEED)
        if self.is_moving_down and not self.is_out_bottom_bound():
            self.rect.move_ip(0, PADDLE_SPEED)

    def is_out_left_bound(self):
        return self.rect.left < 0

    def is_out_right_bound(self):
        return self.rect.right > gs.WIDTH

    def is_out_top_bound(self):
        return self.rect.top < 0

    def is_out_bottom_bound(self):
        return self.rect.bottom > gs.HEIGHT      
