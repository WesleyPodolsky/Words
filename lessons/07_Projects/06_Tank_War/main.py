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

winner = "none"

waveRect = ""

waveRect2 = ""

wave2realx = 350
wave2realy = 300
canshoot2 = False
score2 = 0


listOfWalls = [
            pygame.Rect(10,10,570,10),
            pygame.Rect(10,10,10,430),
            pygame.Rect(580,10,10,430),
            pygame.Rect(10,430,570,10),

            pygame.Rect(275,205,40,40),

            pygame.Rect(120,165,10,120),
            pygame.Rect(110,165,20,10),
            pygame.Rect(110,285,20,10),
            pygame.Rect(150,60,20,20),
            pygame.Rect(150,350,20,20),

            pygame.Rect(460,165,10,120),
            pygame.Rect(460,165,20,10),
            pygame.Rect(460,285,20,10),
            pygame.Rect(400,60,20,20),
            pygame.Rect(400,350,20,20),
            ]



# Initialize Pygame
vel = 0
vely = 0
shootAngle = 0

vel2 = 0
vely2 = 0
shootAngle2 = 0
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
        global winner
        global waveRect

        if winner == "two":
            self.kill()

        waveRect = self.rect

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
                if winner == "none":
                    if keys[pygame.K_a]:
                        vel -= 0.1
                        shootAngle = 90
                    if keys[pygame.K_d]:
                        vel += 0.1
                        shootAngle = 270
                    game_over = True
                    if keys[pygame.K_w]:
                        vely -=0.1
                        shootAngle = 0
                    if keys[pygame.K_s]:
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
            bullet = Bullet(playerx = waverealx-20, playery= waverealy-20, assignedPlayer = "one")
            bullets.add(bullet)
            canshoot = False
            return 1
        return 0

        








class Wave2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.wave = pygame.image.load(images_dir / "tank.png")
        self.image = self.wave
        self.rect = pygame.Rect(550,220,0,0)
        self.image = pygame.transform.scale(self.image, (44, 50))
        self.image = pygame.transform.rotate(self.image, shootAngle)
        self.rect = self.image.get_rect(center=self.rect.center)
        




        

        
        






    def update(self):
        global vel2
        global wave2realx
        global wave2realy
        global canshoot2
        global vely2
        global shootAngle2
        global winner
        global waveRect2

        if winner == "one":
            self.kill()
        
        waveRect2 = self.rect

        self.wave = pygame.image.load(images_dir / "tank.png")
        self.image = self.wave
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.image = pygame.transform.rotate(self.image, shootAngle2)
        wave2realx = self.rect.x +40
        wave2realy = self.rect.y +40
        vel2 = vel2 * 0.95
        vely2 = vely2 * 0.95
        self.rect.x += vel2
        self.rect.y += vely2
        keys = pygame.key.get_pressed()
        if vel2 <= 7:
            if winner == "none":
                if vel2 >= -7:
                    if keys[pygame.K_LEFT]:
                        vel2 -= 0.1
                        shootAngle2 = 90
                    if keys[pygame.K_RIGHT]:
                        vel2 += 0.1
                        shootAngle2 = 270
                    game_over = True
                    if keys[pygame.K_UP]:
                        vely2 -=0.1
                        shootAngle2 = 0
                    if keys[pygame.K_DOWN]:
                        vely2 += 0.1
                        shootAngle2 = 180

                    for wall in listOfWalls:    
                            if self.rect.colliderect(wall):
                                print("touchin wall", random.randint(111,999))
                                vel2 = -1 * vel2
                                break
                    for wall in listOfWalls:    
                            if self.rect.colliderect(wall):
                                print("touchin wall", random.randint(111,999))
                                vely2 = -1 * vely2
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
        global wave2realx
        global wave2realy
        global canshoot2
        if canshoot2:
            bullet = Bullet(playerx = wave2realx-20, playery= wave2realy-20, assignedPlayer = "two")
            bullets.add(bullet)
            canshoot2 = False
            return 1
        return 0













class Bullet(pygame.sprite.Sprite):
    def __init__(self, playerx,playery, assignedPlayer):
        super().__init__()

        self.bull = pygame.image.load(images_dir / "tank.png")
        self.image = self.bull
        self.rect = pygame.Rect(playerx,playery,0,0)
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.assignedPlayer = assignedPlayer

        if assignedPlayer == "one":
            self.angle = shootAngle
        else:
            self.angle = shootAngle2


    def update(self):
        
        print(wave.rect)
        global winner
        global canshoot
        global canshoot2
        global waveRect
        global waveRect2

        if self.angle == 0:
            self.rect.y -= 5
        if self.angle == 90:
            self.rect.x -=5
        if self.angle == 270:
            self.rect.x +=5
        if self.angle == 180:
            self.rect.y += 5

        if self.assignedPlayer == "one":
            if self.rect.colliderect(waveRect2):
                print("Player 2 died")
                winner = "one"

        if self.assignedPlayer == "two":
            if self.rect.colliderect(waveRect):
                print("Player 1 died")
                winner = "two"

                

        if pygame.time.get_ticks() % 100 == 0:
            canshoot = True
            canshoot2 = True

        for wall in listOfWalls:    
            if self.rect.colliderect(wall):
                print("bullet touchin wall", random.randint(111,999))
                self.kill()

        
                

class Button():
    def __init__(self, butx, buty, butwid, buthigh, butcolor, buttext, buttxtcolor, textpadding):
        self.butx = 0
        self.buty = 200
        self.butwid = 40
        self.buthigh = 600
        self.butcolor = "black"
        self.buttext = buttext
        self.buttxtcolor = "orange"
        self.textpadding = 100

    def button_draw(self, buttext, butcolor):
        pygame.draw.rect(screen, self.butcolor, (self.butx, self.buty, self.buthigh, self.butwid))
        buttontext = font.render(buttext, True, butcolor)
        screen.blit(buttontext, (self.butx + self.textpadding, self.buty+((self.butwid-21.67)/2)))

    def button_clicked(self):
            if pygame.mouse.get_pos()[0] > self.butx and pygame.mouse.get_pos()[0] <  self.butx +self.buthigh and pygame.mouse.get_pos()[1] >  self.buty and pygame.mouse.get_pos()[1] <  self.buty + self.butwid and pygame.mouse.get_pressed()[0] == True:

                return True
                
            else:
                return False
            
button = Button(220,100,60,150,'grey',"New Button",'black',20)
        





# Create a player object
wave = Wave()     
wave_group = pygame.sprite.GroupSingle(wave)

wave2 = Wave2()     
wave_group2 = pygame.sprite.GroupSingle(wave2)











# Main game loop
def game_loop():
    global hiscore
    global canshoot
    global canshoot2
    global gamespeed
    global game_over
    global score
    global score2
    global waverealx
    global wave2realx
    global size
    global listOfWalls
    
    button = Button(220,100,60,150,'grey',"New Button",'black',20)
    clock = pygame.time.Clock()

    

    # Group for obstacles
 

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    wave = Wave()
    wave_group.add(wave)

    wave2 = Wave2()
    wave_group2.add(wave2)

    


    bullet_count = 0

    while True:
        while game_over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            

            # Update player

            

            wave.update()

            wave2.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT]:  
                bullet_count += Wave.add_bullet(bullets)
                if pygame.time.get_ticks() % 10 == 0:
                    canshoot = True
            if keys[pygame.K_RSHIFT]:  
                bullet_count += Wave2.add_bullet(bullets)
                if pygame.time.get_ticks() % 10 == 0:
                    canshoot2 = True
                    





            bullets.update()
            enemies.update()

            gamespeed += 0.01
            # Check for collisions


            
                        
            
                

                





            collider2 = pygame.sprite.groupcollide(wave_group, enemies,dokilla=True, dokillb=True)
            if collider2:
                game_over = True
        
            # Draw everything
            screen.fill((222,222,222))
            wave_group.draw(screen)
            wave_group2.draw(screen)
            bullets.draw(screen)
            enemies.draw(screen)

            displayscore = font.render("P1", True, "red")
            screen.blit(displayscore, (waverealx - 35, waverealy+5))

            displayscore = font.render("P2", True, "blue")
            screen.blit(displayscore, (wave2realx - 35, wave2realy+5))

           
            
            



            
            
            for i in range(len(listOfWalls)):
                pygame.draw.rect(screen, (100,100,100), listOfWalls[i], 0)


            if winner == "one":
                button.button_draw(buttext = "Player One Wins!", butcolor = "red")

            if winner == "two":
                button.button_draw(buttext = "Player Two Wins!", butcolor = "lightblue")

            #pygame.draw.rect(screen, (0,0,150), wave.rect, 0)  
            # hitbox for player ^^^

            if winner != "none":
                for bullet in bullets:
                    bullet.kill()

            


        
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

            





game_loop()