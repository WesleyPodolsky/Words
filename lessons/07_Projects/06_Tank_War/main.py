import pygame
from pathlib import Path
import random

FPS = 60

hiscore = 0
game_over = False
waverealx = 350
waverealy = 300
canshoot = False
gamespeed = 1
score = 0
size = 60


listOfWalls = [
            pygame.Rect(10,10,570,10),
            pygame.Rect(10,10,10,430),
            pygame.Rect(580,10,10,430),
            pygame.Rect(10,430,570,10),
            pygame.Rect(120,165,10,120),
            pygame.Rect(110,165,20,10),
            pygame.Rect(110,285,20,10),
            pygame.Rect(150,60,20,20),
            pygame.Rect(150,350,20,20),
            pygame.Rect(170,205,40,40)
            ]



# Initialize Pygame
vel = 0
vely = 0
shootAngle = 0
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
assets = Path(__file__).parent / "images"

# Screen dimensions
WIDTH, HEIGHT = 600, 450
font = pygame.font.SysFont(None, 20)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("invaders")




class Wave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.wave = pygame.image.load(images_dir / "tank.png")
        self.image = self.wave
        self.rect = pygame.Rect(60,220,0,0)
        self.image = pygame.transform.scale(self.image, (44, 50))
        self.image = pygame.transform.rotate(self.image, shootAngle)
        self.rect = self.image.get_rect(center=self.rect.center)
        




        

        
        






    def update(self):
        global vel
        global waverealx
        global waverealy
        global canshoot
        global vely
        global shootAngle

        self.wave = pygame.image.load(images_dir / "tank.png")
        self.image = self.wave
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.image = pygame.transform.rotate(self.image, shootAngle)
        waverealx = self.rect.x +40
        waverealy = self.rect.y +40
        vel = vel * 0.95
        vely = vely * 0.95
        self.rect.x += vel
        self.rect.y += vely
        keys = pygame.key.get_pressed()
        if vel <= 7:
            if vel >= -7:
                if keys[pygame.K_LEFT]:
                    vel -= 0.1
                    shootAngle = 90
                if keys[pygame.K_RIGHT]:
                    vel += 0.1
                    shootAngle = 270
                game_over = True
                if keys[pygame.K_UP]:
                    vely -=0.1
                    shootAngle = 0
                if keys[pygame.K_DOWN]:
                    vely += 0.1
                    shootAngle = 180

                for wall in listOfWalls:    
                        if self.rect.colliderect(wall):
                            print("touchin wall", random.randint(111,999))
                            vel = -1 * vel
                            break
                for wall in listOfWalls:    
                        if self.rect.colliderect(wall):
                            print("touchin wall", random.randint(111,999))
                            vely = -1 * vely
                            break
                    

        if self.rect.x < -20:
            self.rect.x = 557
        if self.rect.x > 557:
            self.rect.x = -20
        if self.rect.y < -5:
            self.rect.y = 405
        if self.rect.y > 405:
            self.rect.y = -5





    def add_bullet(bullets):
        global waverealx
        global waverealy
        global canshoot
        if canshoot:
            bullet = Bullet(playerx = waverealx-20, playery= waverealy-20)
            bullets.add(bullet)
            canshoot = False
            return 1
        return 0

        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, playerx,playery):
        super().__init__()

        self.bull = pygame.image.load(images_dir / "tank.png")
        self.image = self.bull
        self.rect = pygame.Rect(playerx,playery,0,0)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle = shootAngle

    def update(self):
        global canshoot
        if self.angle == 0:
            self.rect.y -= 5
        if self.angle == 90:
            self.rect.x -=5
        if self.angle == 270:
            self.rect.x +=5
        if self.angle == 180:
            self.rect.y += 5

        if pygame.time.get_ticks() % 100 == 0:
            canshoot = True

        for wall in listOfWalls:    
            if self.rect.colliderect(wall):
                print("bullet touchin wall", random.randint(111,999))
                self.kill()
                

        
        





# Create a player object
wave = Wave()     
wave_group = pygame.sprite.GroupSingle(wave)











# Main game loop
def game_loop():
    global hiscore
    global canshoot
    global gamespeed
    global game_over
    global score
    global waverealx
    global size
    global listOfWalls
    
    button = Button(220,100,60,150,'grey',"New Button",'black',20)
    clock = pygame.time.Clock()

    

    # Group for obstacles
 

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    wave = Wave()
    wave_group.add(wave)

    


    bullet_count = 0

    while True:
        while game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            

            # Update player

            

            wave.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:  
                bullet_count += Wave.add_bullet(bullets)
                if pygame.time.get_ticks() % 10 == 0:
                    canshoot = True
                    





            bullets.update()
            enemies.update()

            gamespeed += 0.01
            # Check for collisions


            
                        
            
                

                





            collider2 = pygame.sprite.groupcollide(wave_group, enemies,dokilla=True, dokillb=True)
            if collider2:
                game_over = True
        
            # Draw everything
            screen.fill((225,150,150))
            wave_group.draw(screen)
            bullets.draw(screen)
            enemies.draw(screen)
            displayscore = font.render("P1 - " + str(score), True, "red")
            screen.blit(displayscore, (waverealx - 35, waverealy+5))
            # Display obstacle count



            
            
            for i in range(len(listOfWalls)):
                pygame.draw.rect(screen, (255,0,0), listOfWalls[i], 0)

            #pygame.draw.rect(screen, (0,0,150), wave.rect, 0)  
            # hitbox for player ^^^

        

            


        
            pygame.display.update()
            clock.tick(FPS)

        # Game over screen
        while game_over == True:
            screen.fill("grey")
            button.button_draw()
            print('hi')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos())
        
            pygame.display.update()
            clock.tick(60)

            if button.button_clicked() == True:
                enemies = pygame.sprite.Group()
               
                wave = Wave()
                wave_group.add(wave)

                game_over = False

            



class Button():
    def __init__(self, butx, buty, butwid, buthigh, butcolor, buttext, buttxtcolor, textpadding):
        self.butx = 0
        self.buty = 200
        self.butwid = 40
        self.buthigh = 600
        self.butcolor = "black"
        self.buttext = '                         YOU WERE HIT! CLICK TO RETRY'
        self.buttxtcolor = "orange"
        self.textpadding = 100

    def button_draw(self):
        pygame.draw.rect(screen, self.butcolor, (self.butx, self.buty, self.buthigh, self.butwid))
        buttontext = font.render(self.buttext, True, self.buttxtcolor)
        screen.blit(buttontext, (self.butx + self.textpadding, self.buty+((self.butwid-21.67)/2)))

    def button_clicked(self):
            if pygame.mouse.get_pos()[0] > self.butx and pygame.mouse.get_pos()[0] <  self.butx +self.buthigh and pygame.mouse.get_pos()[1] >  self.buty and pygame.mouse.get_pos()[1] <  self.buty + self.butwid and pygame.mouse.get_pressed()[0] == True:

                return True
                
            else:
                return False
game_loop()