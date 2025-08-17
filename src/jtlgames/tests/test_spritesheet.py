import unittest
import pygame
from spritesheet import SpriteSheet
from pathlib import Path

images  = Path(__file__).parent / 'images'

class TestSpriteSheet(unittest.TestCase):
    """Tests for the SpriteSheet class."""

    def setUp(self):
        """Set up test variables."""
        pygame.init()
        self.filename = images/'spritesheet.png'
        self.cellsize = (16, 16)
        
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        
        self.spritesheet = SpriteSheet(self.filename, self.cellsize)

    def test_xy_to_index(self):
        """Test the xy_to_index method."""
        self.assertEqual(self.spritesheet.xy_to_index(0, 0), 0)
        self.assertEqual(self.spritesheet.xy_to_index(1, 1), 9)
        self.assertEqual(self.spritesheet.xy_to_index(0, 4), 32)

    def test_index_to_xy(self):
        """Test the index_to_xy method."""
        self.assertEqual(self.spritesheet.index_to_xy(10), (10 % (self.spritesheet.sheet.get_width() // self.cellsize[0]), 10 // (self.spritesheet.sheet.get_width() // self.cellsize[0])))

    def test_image_at(self):
        """Test the image_at method."""
        image = self.spritesheet.image_at((0, 0))
        self.assertIsInstance(image, pygame.Surface)

    def test_num_sprites(self):
        """Test the num_sprites property."""
        self.assertEqual(self.spritesheet.num_sprites, (self.spritesheet.sheet.get_width() // self.cellsize[0]) * (self.spritesheet.sheet.get_height() // self.cellsize[1]))

    def test_size(self):
        """Test the size property."""
        self.assertEqual(self.spritesheet.size, (self.spritesheet.sheet.get_width() // self.cellsize[0], self.spritesheet.sheet.get_height() // self.cellsize[1]))

    def test_images_at(self):
        """Test the images_at method."""

        images = self.spritesheet.images_at([(0, 0), (1, 1)])
        self.assertEqual(len(images), 2)
        self.assertIsInstance(images[0], pygame.Surface)
        self.assertIsInstance(images[1], pygame.Surface)

    def test_load_strip(self):
        """Test the load_strip method."""
        
        images = self.spritesheet.load_strip((0, 0), 3)
        self.assertEqual(len(images), 3)
        self.assertIsInstance(images[0], pygame.Surface)
        self.assertIsInstance(images[1], pygame.Surface)
        self.assertIsInstance(images[2], pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

if __name__ == "__main__":
    unittest.main()