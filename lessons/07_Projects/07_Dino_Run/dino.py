"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path
i=0
game_over = False
passedobj = 0
hiscore = 0
# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
assets = Path(__file__).parent / "images"

# Screen dimensions
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Jump")

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)

# FPS
FPS = 60

# Player attributes
PLAYER_SIZE = 50

player_speed = 5

# Obstacle attributes
OBSTACLE_WIDTH = 25
OBSTACLE_HEIGHT = 45
obstacle_speed = 5

# Font
font = pygame.font.SysFont(None, 36)




# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - OBSTACLE_HEIGHT - 10

        self.explosion = pygame.image.load(images_dir / "explosion1.gif")
        self.cactus = pygame.image.load(images_dir / "cactus_10.png")

        self.image = self.cactus
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)

        

    def update(self):
        self.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()
            global passedobj
            passedobj += 1
            

    def explode(self):
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)
        global game_over
        game_over = True
        

    

# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - PLAYER_SIZE - 10
        self.speed = player_speed
        self.vel = 0
        self.isjumping = False

        self.dino = pygame.image.load(images_dir / "dino_0.png")

        self.image = self.dino
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(center=self.rect.center)



    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.isjumping == False:
                self.isjumping = True
                self.vel = 15

    

        # Keep the player on screen
    
            
        
       

        if self.vel > -20 and self.isjumping:
            self.vel -= 1
            self.rect.y -= self.vel
            
        print("Jumping: " + str(self.isjumping)+ " Y: " +str(self.rect.y))


        if self.rect.y > 295:
            self.rect.y = 295
            
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.isjumping = False

        


# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)



# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
    if random.random() < 0.4:
        obstacle = Obstacle()
        obstacles.add(obstacle)
        return 1
    return 0






# Main game loop
def game_loop():
    global game_over
    global passedobj
    global hiscore

    clock = pygame.time.Clock()
    
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()

    button = Button(220,100,60,150,'grey',"New Button",'black',)

    player = Player()
    player_group.add(player)

    obstacle_count = 0
    while True:
        while game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            

            # Update player
            player.update()

            # Add obstacles and update
            if pygame.time.get_ticks() - last_obstacle_time > 500:
                last_obstacle_time = pygame.time.get_ticks()
                obstacle_count += add_obstacle(obstacles)

            
            
                    
            
            obstacles.update()

            # Check for collisions
            collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
            if collider:
                collider[0].explode()
        
            # Draw everything
            screen.fill("white")
            #pygame.draw.rect(screen, BLUE, player)
            obstacles.draw(screen)
            player_group.draw(screen)

            # Display obstacle count
            obstacle_text = font.render(f"score: {passedobj}", True, BLACK)
            screen.blit(obstacle_text, (10, 10))
            if passedobj > hiscore:
                hiscore = passedobj
            obstacle_text = font.render(f"highscore: {hiscore}", True, 'gold')
            screen.blit(obstacle_text, (10, 40))

        


        
            pygame.display.update()
            clock.tick(FPS)

        # Game over screen
        
        while game_over == True:
            screen.fill(WHITE)
            button.button_draw()
            print('hi')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos())
        
            pygame.display.update()
            clock.tick(60)

            if button.button_clicked() == True:
                obstacles = pygame.sprite.Group()
                passedobj = 0
                
                game_over = False



class Button():
    def __init__(self, butx, buty, butwid, buthigh, butcolor, buttext, buttxtcolor):
        self.butx = -200
        self.buty = 100
        self.butwid = 60
        self.buthigh = 700
        self.butcolor = "gray"
        self.buttext = 'you lost! ' \
        'click to retry'
        self.buttxtcolor = BLACK

    def button_draw(self):
        pygame.draw.rect(screen, self.butcolor, (self.butx, self.buty, self.buthigh, self.butwid))
        buttontext = font.render(self.buttext, True, self.buttxtcolor)
        screen.blit(buttontext, (self.butx+((self.buthigh-141.89)/2), self.buty+((self.butwid-21.67)/2)))

    def button_clicked(self):
            if pygame.mouse.get_pos()[0] > self.butx and pygame.mouse.get_pos()[0] <  self.butx +self.buthigh and pygame.mouse.get_pos()[1] >  self.buty and pygame.mouse.get_pos()[1] <  self.buty + self.butwid and pygame.mouse.get_pressed()[0] == True:
                return True
            else:
                return False
                                    

        

        #     def custom_button(custombutx, custombuty, custombutwid,custombuthigh,color,custombuttext,txtcolor):
        #         pygame.draw.rect(screen, color, (custombutx, custombuty, custombuthigh, custombutwid))
        #         buttontext = font.render(custombuttext, True, txtcolor)
        #         screen.blit(buttontext, (custombutx+((custombuthigh-141.89)/2), custombuty+((custombutwid-21.67)/2)))

            

        #         if pygame.mouse.get_pos()[0] > custombutx:
        #             if pygame.mouse.get_pos()[0] < custombutx+custombuthigh:
        #                 if pygame.mouse.get_pos()[1] > custombuty:
        #                     if pygame.mouse.get_pos()[1] < custombuty+custombutwid:
        #                         print('on button')
        #                         if pygame.mouse.get_pressed()[0] == True:
        #                             global game_over
        #                             game_over = False
        #                             obstacles = pygame.sprite.Group()
            
        #     # button Parameters: (x, y, width, height, color, text, textcolor)
        #     #--------------------------------------------------------#
        #     for eveny in pygame.event.get():
        #         if event.type == pygame.MOUSEBUTTONUP:
        #             print(pygame.mouse.get_pos())
        #     print(str(game_over) + "game")   
        #     custom_button(220,100,60,150,'grey',"New Button",'black')
        #     pygame.display.update()
        #     clock.tick(60)
        # #--------------------------------------------------------#
        


 





if __name__ == "__main__":
    game_loop()
    

    