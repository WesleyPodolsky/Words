import pygame


class Pad(pygame.sprite.Sprite):
    def __init__(self, x, y, tall=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('resources/landing_pads/pad' + ('_tall' if tall else '') + '.png')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
