import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path

images = Path(__file__).parent / 'images'



def scale_sprites(sprites, scale):
    """Scale a list of sprites by a given factor.

    Args:
        sprites (list): List of pygame.Surface objects.
        scale (int): Scale factor.

    Returns:
        list: List of scaled pygame.Surface objects.
    """
    return [pygame.transform.scale(sprite, (sprite.get_width() * scale, sprite.get_height() * scale)) for sprite in sprites]

def main():
    global bgimage
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Sprite Animation Test")

    # Load the sprite sheet
    filename = images / 'spritesheet.png'  # Replace with your actual file path
    cellsize = (16, 16)  # Replace with the size of your sprites
    spritesheet = SpriteSheet(filename, cellsize)


    # Load a strip sprites
    frog_sprites = scale_sprites(spritesheet.load_strip(0, 4, colorkey=-1) , 4)
    allig_sprites = scale_sprites(spritesheet.load_strip( (0,4), 7, colorkey=-1), 4)

    # Compose an image
    log = spritesheet.compose_horiz([24, 25, 26], colorkey=-1)
    log = pygame.transform.scale(log, (log.get_width() * 4, log.get_height() * 4))

    # Variables for animation
    frog_index = 0
    allig_index = 0
    frames_per_image = 6
    frame_count = 0

    class Gator(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()


            self.rect = pygame.Rect(100,100,75,50)


        def gator_update(self):
            print(self.rect)
            print(frog.rect)
            
            if self.rect.x < frog.rect.x:
                self.rect.x += 1
                print('1')
            if self.rect.x >= frog.rect.x:
                self.rect.x -= 1
                print('2')
            if self.rect.y >= frog.rect.y:
                self.rect.y -= 1
                print('3')
            if self.rect.y < frog.rect.y:
                self.rect.y += 1
                print('4')
          


    class Frog(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()


            self.rect = frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            self.jump = 19
            self.move=0

        def frog_jump():
            global frog_index
            frog_index = 0
            return frog_index
        
        def update_frog(self):
            if self.jump < 20 and self.move == 1:
                self.rect.y -= 6
                
            if self.jump < 20 and self.move == 2:
             
                self.rect.x += 6
            if self.jump < 20 and self.move == 3:
               
                self.rect.y += 6
            if self.jump < 20 and self.move == 4:
                
                self.rect.x -= 6

    
            

            


    # Main game loop
    running = True
    
    frog = Frog()
    gator = Gator()

    

    sprite_rect = frog_sprites[0].get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    
    pygame.math.Vector2(1, 0)
    def draw_alligator(alligator, index):
        """Creates a composed image of the alligator sprites.

        Args:
            alligator (list): List of alligator sprites.
            index (int): Index value to determine the right side sprite.

        Returns:
            pygame.Surface: Composed image of the alligator.
        """
        
        index = index % (len(alligator)-2)
        
        width = alligator[0].get_width()
        height = alligator[0].get_height()
        composed_image = pygame.Surface((width * 3, height), pygame.SRCALPHA)


        composed_image.blit(alligator[0], (0, 0))
        composed_image.blit(alligator[1], (width, 0))
        composed_image.blit(alligator[(index + 2) % len(alligator)], (width * 2, 0))

        return composed_image
    


            


    while running:
        screen.fill((0, 0, 139))  # Clear screen with deep blue

        

        bgimage = images / 'frogger.png'
        orig_image= pygame.image.load(bgimage).convert()
        orig_image = pygame.transform.scale(orig_image, (640, 480))
        screen.blit(orig_image, (10,10))





        Gator.gator_update(gator)
        # Update animation every few frames
        frame_count += 1
        
        if frame_count % frames_per_image == 0: 
            if frog_index < 2:
                frog_index = (frog_index + 1) % len(frog_sprites)
            allig_index = (allig_index + 1) % len(allig_sprites)
        # Get the current sprite and display it in the middle of the screen
        frog.jump += 0.1
        

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and frog.jump > 21 :
            frog.jump= 19
            frog.move = 1
            Frog.frog_jump()
            frog_index = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and frog.jump > 21 :
            frog.jump= 19
            frog.move = 2
            Frog.frog_jump()
            frog_index = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and frog.jump > 21 :
            frog.jump= 19
            frog.move = 3
            Frog.frog_jump()
            frog_index = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and frog.jump > 21 :
            frog.jump= 19
            frog.move = 4
            Frog.frog_jump()
            frog_index = 0
                
        Frog.update_frog(frog)

        frog2x =(frog_sprites[frog_index])
        screen.blit(frog2x, frog.rect)

        composed_alligator = draw_alligator(allig_sprites, allig_index)
        screen.blit(composed_alligator,  (gator.rect.x-120, gator.rect.y, 10, 10))

        screen.blit(log,  sprite_rect.move(0, -100))
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            pygame.draw.rect(screen, "brown", gator.rect)
            pygame.draw.rect(screen, "green", frog.rect)

        # Update the display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Cap the frame rate
        pygame.time.Clock().tick(60)

        if frog.rect.colliderect(gator.rect):
            pygame.quit()

    

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
