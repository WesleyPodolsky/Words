import pygame
from pathlib import Path
import random

shootAngle = 9
game_over = False
vel = 0
vely = 0
gamespeed = 1
score = 0


FPS = 60

pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
assets = Path(__file__).parent / "images"

# Screen dimensions
WIDTH, HEIGHT = 600, 450
font = pygame.font.SysFont(None, 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("lander")




class Wave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.wave = pygame.image.load(images_dir / "lander.png")
        self.image = self.wave
        self.rect = pygame.Rect(300,20,0,0)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.image = pygame.transform.rotate(self.image, shootAngle)
        self.rect = self.image.get_rect(center=self.rect.center)
        




        

        
        






    def update(self):
        global vel
        global vely
        global shootAngle
        global waverealx
        global waverealy

        global score


        if self.rect.y < 310:
            print("falling", random.randint(0,1))
            vely += 0.1
        else:
            self.rect.y = 309
            print("on ground")

            score = 10-vely


        self.wave = pygame.image.load(images_dir / "lander.png")
        self.image = self.wave
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image = pygame.transform.rotate(self.image, shootAngle)
        waverealx = self.rect.x +40
        waverealy = self.rect.y +40
        vel = vel * 0.99
        vely = vely * 0.99
        self.rect.x += vel
        self.rect.y += vely
        keys = pygame.key.get_pressed()
        if vel <= 7:
            if vel >= -7:
                if keys[pygame.K_LEFT]:
                    vel -= 0.1
                if keys[pygame.K_RIGHT]:
                    vel += 0.1
                if keys[pygame.K_UP]:
                    vely -=0.3
                    shootAngle = 0
                if keys[pygame.K_DOWN]:
                    vely += 0.1

                
                    

        if self.rect.x < -20:
            self.rect.x = 557
        if self.rect.x > 557:
            self.rect.x = -20
        if self.rect.y < -5:
            self.rect.y = 405
        if self.rect.y > 405:
            self.rect.y = -5



# Create a player object
wave = Wave()     
wave_group = pygame.sprite.GroupSingle(wave)











# Main game loop
def game_loop():
    global canshoot
    global gamespeed
    global game_over
    global score
    global vely
    
    clock = pygame.time.Clock()

    

    # Group for obstacles
 

    enemies = pygame.sprite.Group()
    
    wave = Wave()
    wave_group.add(wave)


    while True:
        while game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            

            # Update player

            
            wave.update()


                    




            # Check for collisions


                

                





            collider2 = pygame.sprite.groupcollide(wave_group, enemies,dokilla=True, dokillb=True)
            if collider2:
                game_over = True
        
            # Draw everything
            screen.fill("black")
            wave_group.draw(screen)

            pygame.draw.rect(screen, 'darkgray', (0, 350, 600, 600))

            enemies.draw(screen)
            displayscore = font.render("score: " + str(score), True, "gold")
            screen.blit(displayscore, (waverealx -22, waverealy+25))
            # Display obstacle count
        

        


        
            pygame.display.update()
            clock.tick(FPS)

        while game_over == True:
            screen.fill("grey")
            print('hi')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos())
        
            pygame.display.update()
            clock.tick(60)


                



game_loop()