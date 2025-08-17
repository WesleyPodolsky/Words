import pygame
from pathlib import Path

class SpriteSheet(object):
    """Class to handle loading and parsing a sprite sheet image.
    """
    def __init__(self, filename, cellsize, offset=(0,0)):
        """
        Initializes the SpriteSheet object.
        Args:
            filename (str): The path to the image file containing the spritesheet.
            cellsize (tuple): The size of each cell in the spritesheet (width, height).
            offset (tuple, optional): The offset to start reading the spritesheet from (x, y). Defaults to (0, 0).
        Raises:
            FileNotFoundError: If the spritesheet image cannot be loaded.
        """
        self.cellsize = cellsize
        
        try:
            
            img = pygame.image.load(filename)
            
            if offset != (0,0):
                img = img.subsurface(pygame.Rect(offset, (img.get_width() - offset[0], img.get_height() - offset[1])))
                    
            try:
                self.sheet = img.convert()
            except pygame.error as e:
                # Probably can't convert because video mode is not set yet. 
                self.sheet = img
            
        except pygame.error as e:
            print(f'Unable to load spritesheet image: {filename}')
            raise FileNotFoundError(e)
        
    def xy_to_index(self, x, y):
        """Converts (x, y) grid position to sprite index"""
  
        cols = self.sheet.get_width() // self.cellsize[0]
        return y * cols + x
    
    def index_to_xy(self, index):

        if isinstance(index, int):
            cols = self.sheet.get_width() // self.cellsize[0]
            x = index % cols
            y = index // cols
        else:
            x, y = index
            
        return x,y

    
    def image_at(self, index, colorkey=None):
        """Loads image from a sprite index (x, y grid position)"""
        
        x,y = self.index_to_xy(index)
        rect = pygame.Rect(x * self.cellsize[0], y * self.cellsize[1], *self.cellsize)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        
        if colorkey is not None: # Set the transparency color?
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        
        return image



    @property
    def num_sprites(self):
        """Returns the number of sprites in the sprite sheet"""
        return (self.sheet.get_width() // self.cellsize[0]) * (self.sheet.get_height() // self.cellsize[1])

    @property
    def size(self):
        """Returns the size of the sprite sheet"""
        
        # sheet_size
        x,y = self.sheet.get_size()
        
        return x // self.cellsize[0], y // self.cellsize[1]

    def images_at(self, indices, colorkey=None):
        """Loads multiple images, supply a list of (x, y) indices"""
        return [self.image_at(index, colorkey) for index in indices]

    def compose_horiz(self, indices, colorkey=None):
        """Creates a composed image of the sprites at the given indices, stacking the spritest from left to right. """
            
        images = self.images_at(indices, colorkey)
        width = sum(image.get_width() for image in images)
        height = images[0].get_height()
        
        composed_image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        x = 0
        for image in images:
            composed_image.blit(image, (x, 0))
            x += image.get_width()
        
        return composed_image

    def load_strip(self, start_index, image_count, colorkey=None):
        """Loads a strip of images starting at start_index (x, y) and returns them as a list"""

        if not isinstance(start_index, int):
            start_index = self.xy_to_index(*start_index)

        return [self.image_at(start_index+i, colorkey) for i in range(image_count)]

    def __str__(self) -> str:
        width, height = self.sheet.get_size()
        return f"SpriteSheet(sheet size: (w={width}, y={height}), cell size: {self.cellsize}, {width // self.cellsize[0]}x{height // self.cellsize[1]} cells)"  

