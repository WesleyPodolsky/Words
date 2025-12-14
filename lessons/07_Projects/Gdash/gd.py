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
tick = 0
player_dead = False
player_win = False
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
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
obstacle_speed = 5

# Font
font = pygame.font.SysFont(None, 36)



background_image = pygame.image.load(images_dir / 'background.jpg').convert()
background_image = pygame.transform.smoothscale(background_image, (WIDTH, HEIGHT))


matrixEnd = (
("e","e","e","e","e","e","e","e","e","e","e","e"),
("e","e","e","e","e","e","e","e","e","e","e","e"),
("e","e","e","e","e","e","e","e","e","e","e","e"),
("e","e","e","e","e","e","e","e","e","e","e","e"),
("e","e","e","e","e","e","e","e","e","e","e","e"),
("e","e","e","e","e","e","e","e","e","e","e","e"),
)



matrixFive = (
("o","o","o","o","o","o","o","o","s","o","o","o"),
("o","o","o","o","o","o","o","o","g","o","o","o"),
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","o","o","g","o","o","o","o","o"),
("o","o","o","o","g","o","g","o","o","g","o","o"),
("g","g","g","s","g","s","g","s","s","g","s","s"),
)

matrixFour = (
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","o","o","s","s","o","o","o","o"),
("o","o","o","o","o","o","g","g","o","o","o","o"),
("o","o","g","g","o","o","o","o","o","o","g","g"),
("g","s","g","g","g","g","g","g","g","g","g","g"),
)

matrixThree = (
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","s","o","g","g","g","o","o","o"),
("o","s","g","g","g","o","g","g","g","s","s","g"),
)

matrixTwo = (
("o","o","o","o","g","g","o","o","o","o","o","g"),
("o","o","o","o","g","g","o","o","o","o","o","g"),
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","o","o","o","o","o","o","o","o","o","o"),
("o","o","g","o","o","o","o","o","o","g","g","o"),
("g","s","g","s","g","s","s","g","s","g","g","s"),
)

matrixOne = (
("o","o","o","o","o","o","o","o","o","g","o","o"),
("o","o","o","o","o","o","o","o","o","g","s","s"),
("o","o","o","o","o","o","o","o","o","o","g","g"),
("o","o","o","o","o","o","g","g","o","o","o","o"),
("o","o","o","g","g","o","g","g","o","o","o","o"),
("g","g","o","g","g","o","g","g","o","o","g","g"),
)

class EndTexture(pygame.sprite.Sprite):
    def __init__(self, spawnx, spawny):
        super().__init__()
        self.rect = pygame.Rect(spawnx,spawny,50,50 )

        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)

        self.endimg = pygame.image.load(images_dir / "endTex.png")
        self.image = self.endimg
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.hei = 50
        self.wid = 50

    def update(self):
        global player_dead
        if player_dead == False:
            self.rect.x -= 5

        if player_dead:
            if self.hei > 1:
                self.image = pygame.transform.scale(self.image, (self.wid, self.hei))
                self.hei -= 1
                self.wid -= 1


class SpikeTexture(pygame.sprite.Sprite):
    def __init__(self, spawnx, spawny):
        super().__init__()
        self.rect = pygame.Rect(spawnx,spawny,50,50 )

        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)

        self.spikeimg = pygame.image.load(images_dir / "spiketexture.png")
        self.image = self.spikeimg
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.hei = 50
        self.wid = 50

    def update(self):
        global player_dead
        if player_dead == False:
            self.rect.x -= 5

        if player_dead:
            if self.hei > 1:
                self.image = pygame.transform.scale(self.image, (self.wid, self.hei))
                self.hei -= 1
                self.wid -= 1


class Spike(pygame.sprite.Sprite):
    def __init__(self, spawnx, spawny):
        super().__init__()
        self.rect = pygame.Rect(spawnx,spawny,10,20)

        self.image = pygame.Surface((20, 50))
        self.image.fill(BLACK)

        self.spikeimg = pygame.image.load(images_dir / "spikehit.png")
        self.image = self.spikeimg
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.rect = self.image.get_rect(center=self.rect.center)

        

    def update(self):
        global player_dead
        if player_dead == False:
            self.rect.x -= 5

        if self.rect.x < -50:
            self.kill()

       

    


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, spawnx, spawny):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = spawnx
        self.rect.y = spawny

        self.explosion = pygame.image.load(images_dir / "explosion1.gif")
        self.cactus = pygame.image.load(images_dir / "block.png")

        self.image = self.cactus
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.hei = 50
        self.wid = 50

        

    def update(self):
        global player_dead
        if player_dead == False:
            self.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()
            global passedobj

        if player_dead:
            if self.hei > 1:
                self.image = pygame.transform.scale(self.image, (self.wid, self.hei))
                self.hei -= 1
                self.wid -= 1

            
            

        if self.rect.x < -50:
            self.kill()
            

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
        self.standing = False
        self.hei = 50
        self.wid = 50

        self.dino = pygame.image.load(images_dir / "gd.jpeg")

        self.image = self.dino
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(center=self.rect.center)

    

    def stand(self):
        self.standing = True
        self.vel = 0
        self.isjumping = False
        
    def fall(self):
        self.standing = False
        if self.rect.y < 249:
            self.isjumping = True
    def update(self):
        if player_win:
            self.image = pygame.transform.scale(self.image, (self.wid, self.hei))
            self.hei +=2
            self.wid -= 0.3
            self.rect.y -= self.hei/10



        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.isjumping == False:
                self.isjumping = True
                self.standing = False
                self.vel = 15

        if self.vel > -20 and self.isjumping:
            
            if self.standing == False:
                self.vel -= 1
                self.rect.y -= self.vel
            
        #print("Jumping: " + str(self.isjumping)+ " Y: " +str(self.rect.y))


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



class Button():
    def __init__(self, butx, buty, butwid, buthigh, butcolor, buttext, buttxtcolor, textpadding):
        self.butx = 0
        self.buty = 200
        self.butwid = 40
        self.buthigh = 600
        self.butcolor = "black"
        self.buttext = buttext
        self.buttxtcolor = "orange"
        self.textpadding = 150

    def button_draw(self, text, butcolor):
        pygame.draw.rect(screen, self.butcolor, (self.butx, self.buty, self.buthigh, self.butwid))
        buttontext = font.render(text, True, butcolor)
        screen.blit(buttontext, (self.butx + self.textpadding, self.buty+((self.butwid-21.67)/2)))

    def button_clicked(self):
            if pygame.mouse.get_pos()[0] > self.butx and pygame.mouse.get_pos()[0] <  self.butx +self.buthigh and pygame.mouse.get_pos()[1] >  self.buty and pygame.mouse.get_pos()[1] <  self.buty + self.butwid and pygame.mouse.get_pressed()[0] == True:

                return True
                
            else:
                return False
            

















# Add obstacles periodically
def add_obstacle(obstacles,x,y):
        obstacle = Obstacle(spawnx=x, spawny=y)
        obstacles.add(obstacle)

#//////////#-#//////////#-#//////////#
spiketextures = pygame.sprite.Group()
endtextures = pygame.sprite.Group()
#//////////#-#//////////#-#//////////#

def add_spike(spikes, x, y):

    spike = Spike(spawnx=x, spawny=y)
    spikes.add(spike)
    add_spiketexture(spiketextures, x= x-20, y = y-20)

def add_spiketexture(spiketextures, x, y):

    spiketexture = SpikeTexture(spawnx=x, spawny=y)
    spiketextures.add(spiketexture)

def add_endtexture(endtextures, x, y):

    endtexture = EndTexture(spawnx=x-20, spawny=y-20)
    endtextures.add(endtexture)



def spawnMatrix(obstacles,spikes,endtextures):
    global matrixOne
    global matrixTwo
    global matrixThree

    chosenMatrix = random.randint(1,5)

    if passedobj > 20:
        chosenMatrix = matrixEnd
    elif chosenMatrix == 1:
        chosenMatrix = matrixOne
    elif chosenMatrix == 2:
        chosenMatrix = matrixTwo
    elif chosenMatrix == 3:
        chosenMatrix = matrixThree
    elif chosenMatrix == 4:
        chosenMatrix = matrixFour
    elif chosenMatrix == 5:
        chosenMatrix = matrixFive


    for y in range(6):
        for x in range(12):
            if chosenMatrix[y][x] == "g":
                matrixSpawnX = 600 + (50 * x)
                matrixSpawnY = 50 * y
                add_obstacle(obstacles,x=matrixSpawnX,y=matrixSpawnY)
                #print("spawned cube at ", matrixSpawnX, ",", matrixSpawnY)

            if chosenMatrix[y][x] == "s":
                matrixSpawnX = 620 + (50 * x)
                matrixSpawnY = (50 * y) +20
                add_spike(spikes,x=matrixSpawnX,y=matrixSpawnY)

            if chosenMatrix[y][x] == "e":
                matrixSpawnX = 620 + (50 * x)
                matrixSpawnY = (50 * y) +20
                add_endtexture(endtextures,x=matrixSpawnX,y=matrixSpawnY)
                #print("spawned spike at ", matrixSpawnX, ",", matrixSpawnY)




# Main game loop
def game_loop():
    global game_over
    global passedobj
    global hiscore
    global tick
    global player_dead
    global player_win

    button = Button(220,100,60,150,'grey',"New Button",'black',100)
    clock = pygame.time.Clock()



    
    
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    
    

    player = Player()
    def createPlayer():
        player_group.add(player)

    createPlayer()
    
    

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


#>----------------------------spawning---------------------------------<#
            
            
            
            #add_obstacle(obstacles,x=200,y=200)
            
            #add_spike(spikes, x= 500, y = 200)

            
            

#>--------------------------------------------------------------------<#


            keys = pygame.key.get_pressed()
            obstacles.update()
            spikes.update()
            spiketextures.update()
            endtextures.update()

            # Check for collisions
            collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
            if collider:
                player.stand()
            else:
                player.fall()

            for index in obstacles:
                collider2 = pygame.sprite.collide_rect(player, index)
                if collider2:
                    #print("-")
                    if index.rect.y < player.rect.y + 20:
                        #print("X")
                        player.kill()
                        player_dead = True

            collider3 = pygame.sprite.spritecollide(player, endtextures, dokill=False)
            if collider3:
                player_win = True
                        

            for index in spikes:
                collider3 = pygame.sprite.collide_rect(player, index)
                if collider3:
                    player.kill()
                    player_dead = True

            if tick % 200 == 0:
                spawnMatrix(obstacles,spikes,endtextures)
    

            tick = tick+1

            if player_dead == False:
                passedobj = round(tick/20)



            if button.button_clicked():
                if player_dead == True:
                    for spike in spikes: spike.kill()
                    for obstacle in obstacles: obstacle.kill()
                    for spiketexture in spiketextures: spiketexture.kill()
                    for endtexture in endtextures: endtexture.kill()
                    createPlayer()
                    player_dead = False
                    player.isjumping = False
                    passedobj = 0
                    tick = 0
                



        
            # Draw everything
            screen.fill("lightblue")
            screen.blit(background_image, (0, 0))

            
            
            obstacles.draw(screen)
            
            player_group.draw(screen)


            scoreRectBg = pygame.Rect(220,10,200,20)
            pygame.draw.rect(screen, BLACK, scoreRectBg)
            scoreRect = pygame.Rect(220,11,passedobj*2,18)
            pygame.draw.rect(screen, WHITE, scoreRect)
            

            #hitbox
            #for spike in spikes:
            #    pygame.draw.rect(screen, BLUE, spike)

            
            spiketextures.draw(screen)
            endtextures.draw(screen)
            #spikes.draw(screen)


            # Display obstacle count
            obstacle_text = font.render(f" {passedobj} %", True, WHITE)
            screen.blit(obstacle_text, (150, 10))
            if passedobj > hiscore:
                hiscore = passedobj
            obstacle_text = font.render(f"highscore: {hiscore}", True, 'gold')

            if player_dead:
                button.button_draw(text="You Died! Click to Retry", butcolor="lime")
            #screen.blit(obstacle_text, (10, 40))

            
               

        


        
            pygame.display.update()
            clock.tick(FPS)

        # Game over screen
        
        while game_over == True:
            screen.fill(WHITE)
    
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    #print(pygame.mouse.get_pos())
                    print("")

        
            pygame.display.update()
            clock.tick(60)

            



                                    

        

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
    

    