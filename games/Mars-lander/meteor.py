import pygame
import random
from config import *


class Meteor(pygame.sprite.Sprite):
    # all meteor images are loaded here, so the game does not load an image on every meteor spawn.
    meteors = [
        pygame.image.load('resources/meteors/spaceMeteors_001.png'),
        pygame.image.load('resources/meteors/spaceMeteors_002.png'),
        pygame.image.load('resources/meteors/spaceMeteors_003.png'),
        pygame.image.load('resources/meteors/spaceMeteors_004.png'),
    ]

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(Meteor.meteors)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._off_screen = False
        self._veloc_x = random.uniform(-3, 3)
        self._veloc_y = random.uniform(0, 3)
        self._x_pixels_to_move = 0
        self._y_pixels_to_move = 0

    def is_off_screen(self):
        """Returns True if the meteor is not on the screen anymore."""
        return self._off_screen

    def move(self):
        """X and Y velocities are added up on every tick. Once they are greater than 1.0 or less than -1.0
           - ergo one pixel on screen, the meteor moves by an integer in the appropriate direction."""
        self._x_pixels_to_move += self._veloc_x
        self._y_pixels_to_move += self._veloc_y

        # move right
        if self._x_pixels_to_move > 1:
            self.rect.move_ip(self._x_pixels_to_move, 0)
            self._x_pixels_to_move -= int(self._x_pixels_to_move)
        # move left
        elif self._x_pixels_to_move < -1:
            self.rect.move_ip(self._x_pixels_to_move, 0)
            self._x_pixels_to_move += int(abs(self._x_pixels_to_move))

        # move down
        if self._y_pixels_to_move > 1:
            self.rect.move_ip(0, self._y_pixels_to_move)
            self._y_pixels_to_move -= int(self._y_pixels_to_move)

    def update(self, *args):
        """Operations executed on every tick."""
        self.move()
        # delete meteor if it flies off the screen or hits surface
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self._off_screen = True
