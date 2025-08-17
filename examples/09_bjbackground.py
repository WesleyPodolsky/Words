import pygame
import random
from pathlib import Path

d = Path(__file__).parent # The directory that holds the script

# Initialize Pygame
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PLAYER_SIZE = 50
    OBSTACLE_WIDTH = 50
    OBSTACLE_HEIGHT = 50
    OBSTACLE_SPEED = 10
    GRAVITY = 1
    JUMP_STRENGTH = 15
    BACKGROUND_SCROLL_SPEED = 2
    FPS = 30

# Initialize screen
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

# Define background class
class Background(pygame.sprite.Sprite):
    """Represents the scrolling background in the game."""
    def __init__(self):
        super().__init__()
        
        # The Sprite image is 2x as wide as the screen
        self.image = pygame.Surface((Settings.SCREEN_WIDTH * 2, Settings.SCREEN_HEIGHT))
        
        # Load the background image and scale it to the screen size. Note the convert() call. 
        # This converts the form of the image to be more efficient. 
        orig_image= pygame.image.load(d/'assets/background.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        
        # Then, copy it into the self.image surface twice
        self.image.blit(orig_image, (0, 0))
        self.image.blit(orig_image, (Settings.SCREEN_WIDTH, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        """Update the position of the background."""
        
        self.rect.x -= Settings.BACKGROUND_SCROLL_SPEED
        
        if self.rect.right <= Settings.SCREEN_WIDTH:
            self.rect.x = 0

# Define player class
class Player(pygame.sprite.Sprite):
    """Represents the player in the game."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Settings.PLAYER_SIZE, Settings.PLAYER_SIZE))
        self.image.fill(Settings.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = Settings.SCREEN_HEIGHT - Settings.PLAYER_SIZE
        self.y_velocity = 0
        self.is_jumping = False

    def update(self):
        """Update the player's position."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.y_velocity = -Settings.JUMP_STRENGTH
            self.is_jumping = True

        self.y_velocity += Settings.GRAVITY
        self.rect.y += self.y_velocity

        if self.rect.bottom >= Settings.SCREEN_HEIGHT:
            self.rect.bottom = Settings.SCREEN_HEIGHT
            self.y_velocity = 0
            self.is_jumping = False


class Obstacle(pygame.sprite.Sprite):
    """Represents an obstacle in the game."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Settings.OBSTACLE_WIDTH, Settings.OBSTACLE_HEIGHT))
        self.image.fill(Settings.BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = Settings.SCREEN_WIDTH
        self.rect.y = Settings.SCREEN_HEIGHT - Settings.OBSTACLE_HEIGHT

    def update(self):
        """Update the position of the obstacle."""
        self.rect.x -= Settings.OBSTACLE_SPEED
        if self.rect.x + Settings.OBSTACLE_WIDTH <= 0:
            self.kill()


class Game:
    """Represents the main game."""
    def __init__(self):
        """Initialize the game, create game objects, and set up the game environment."""
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        # Create background instance and add to sprite group
        self.background = Background()
        self.all_sprites.add(self.background)

        # Create player instance and add to sprite group
        self.player = Player()
        self.all_sprites.add(self.player)

        # Score
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)

        # Clock
        self.clock = pygame.time.Clock()

    def run(self):
        """Run the main game loop."""
        running = True
        obstacle_counter = 0 #Enforce a min number of frames between obstacles. 

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.all_sprites.update()

            # Draw everything
            self.all_sprites.draw(screen)

            # Spawn obstacles. The `obstacle_counter` is used to enforce a
            # minimum number of frames between obstacles. The  `
            # obstacle_counter % 30 == 0` means that there is an
            # opportunity to spawn an obstacle every 30 frames , but the actual
            # spawn rate is controlled by the random.random() call. So this code
            # has a 40% chance of spawning an obstacle every 30 frames.
            if random.random() <= .4 and obstacle_counter % 30 == 0:
                obstacle = Obstacle()
                self.obstacles.add(obstacle)
                self.all_sprites.add(obstacle)
          
            obstacle_counter += 1

            # Check for collisions
            if (collider := pygame.sprite.spritecollideany(self.player, self.obstacles)):
                collider.image.fill((255, 0, 0))  # Make sprites red when they collide

            # Draw score
            self.score += 1
            score_text = self.font.render(f"Score: {self.score}", True, Settings.BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            
            self.clock.tick(Settings.FPS)

        pygame.quit()


def main():
    """Create a game instance and run it."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
