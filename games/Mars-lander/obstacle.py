import pygame
import random


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        obstacles_list = [
            'building_dome',
            'building_station_NE',
            'building_station_SW',
            'pipe_ramp_NE',
            'pipe_stand_SE',
            'rocks_NW',
            'rocks_ore_SW',
            'rocks_small_SE',
            'satellite_SE',
            'satellite_SW'
        ]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/obstacles/' + random.choice(obstacles_list) + '.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
