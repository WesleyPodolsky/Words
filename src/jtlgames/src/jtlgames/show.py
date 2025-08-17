"""Display a spritesheet expanded to a larger size.

"""

import pygame
from pathlib import Path
from .spritesheet import SpriteSheet


class SpriteShow:
    """Class to display an expanded spritesheet.

    Attributes:
        spritesheet (SpriteSheet): The spritesheet object.
        screen_width (int): The width of the display screen.
        screen_height (int): The height of the display screen.
    """

    def __init__(self, screen,  filename, cellsize, offset=(0, 0)):
        self.ss = SpriteSheet(filename, cellsize, offset)
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

    def sprite_pos(self, index):
        """Returns the screen position of a sprite index, where we will draw the sprite."""
        cell_x = self.ss.cellsize[0] * 2 + 20
        cell_y = self.ss.cellsize[1] * 2 + 20
        cols = self.screen_width // cell_x
        row, col = divmod(index, cols)
        x = col * cell_x + 20
        y = row * cell_y + 20
        return x, y

    def draw_sprite(self, sprite, index):
        x, y = self.sprite_pos(index)
        self.screen.blit(sprite, (x, y))

    def text_pos(self, index):
        x, y = self.sprite_pos(index)
        return x, y + self.ss.cellsize[1] * 2 + 3

    def draw_text(self, text, index):
        x, y = self.text_pos(index)
        font = pygame.font.Font(None, 20)
        text = font.render(text, True, (255, 255, 255))
        self.screen.blit(text, (x, y))

    def show(self):
        self.screen.fill((0, 0, 0))
        for i in range(self.ss.num_sprites):
            sprite = self.ss.image_at(i, colorkey=-1)
            sprite = pygame.transform.scale(sprite, (self.ss.cellsize[0] * 2, self.ss.cellsize[1] * 2))
            self.draw_sprite(sprite, i)
            self.draw_text(str(i), i)

        running = True
        while running:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        pygame.quit()


    
    
