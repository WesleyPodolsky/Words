import pygame
from pathlib import Path
import random

FPS = 60

hiscore = 0
game_over = False
waverealx = 350
canshoot = False
gamespeed = 1
score = 0
# Initialize Pygame
vel = 0
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
assets = Path(__file__).parent / "images"

# Screen dimensions
WIDTH, HEIGHT = 600, 450
font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("invaders")




class Wave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.wave = pygame.image.load(images_dir / "wave.png")
        self.image = self.wave
        self.rect = pygame.Rect(300,420,0,0)
        self.image = pygame.transform.scale(self.image, (44, 50))
        self.rect = self.image.get_rect(center=self.rect.center)




        

        
        






    def update(self):
        global vel
        global waverealx
        global canshoot
        waverealx = self.rect.x +20
        vel = vel * 0.99
        self.rect.x += vel
        keys = pygame.key.get_pressed()
        if vel <= 7:
            if vel >= -7:
                if keys[pygame.K_LEFT]:
                    vel -= 0.1
                if keys[pygame.K_RIGHT]:
                    vel += 0.1

        if self.rect.x < -20:
            self.rect.x = 600
        if self.rect.x > 600:
            self.rect.x = -20

        





    def add_bullet(bullets):
        global waverealx
        global canshoot
        if canshoot:
            bullet = Bullet(playerx = waverealx)
            bullets.add(bullet)
            canshoot = False
            return 1
        return 0

        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, playerx):
        super().__init__()

        self.bull = pygame.image.load(images_dir / "face.png")
        self.image = self.bull
        self.rect = pygame.Rect(playerx,400,0,0)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        global canshoot
        self.rect.y -= 4
        if pygame.time.get_ticks() % 20 == 0:
            canshoot = True

        
        


class Enemy(pygame.sprite.Sprite):
    def __init__(self, spawnx):
        super().__init__()

        self.bull = pygame.image.load(images_dir / "demonface.png")
        self.image = self.bull
        self.rect = pygame.Rect(spawnx,0,0,0)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        global game_over
        self.rect.y += 0.5+gamespeed/25

        if self.rect.y > 450:
            print("game over")
            game_over = True

    def add_enemy(enemies):
        enemy = Enemy(spawnx = random.randint(25,575))
        enemies.add(enemy)
        return 1
    
    def explode(self):
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
    
    button = Button(220,100,60,150,'grey',"New Button",'black',20)
    clock = pygame.time.Clock()

    

    # Group for obstacles
 

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    
    wave = Wave()
    wave_group.add(wave)

    
    enemy_count = 0
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
                if pygame.time.get_ticks() % 100 == 0:
                    canshoot = True
                    
            if random.randint(0,1000) <= gamespeed:
                enemy_count += Enemy.add_enemy(enemies)




            bullets.update()
            enemies.update()
            gamespeed += 0.01
            # Check for collisions
            collider = pygame.sprite.groupcollide(bullets, enemies,dokilla=True, dokillb=True)
            if collider:
                score += 1
                print("boom")
        
            # Draw everything
            screen.fill("blue")
            wave_group.draw(screen)
            bullets.draw(screen)
            enemies.draw(screen)
            displayscore = font.render("score: " + str(score), True, "gold")
            screen.blit(displayscore, (waverealx -40, 350))
            # Display obstacle count
        

        


        
            pygame.display.update()
            clock.tick(FPS)

        # Game over screen
        while game_over == True:
            screen.fill("blue")
            button.button_draw()
            print('hi')
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    print(pygame.mouse.get_pos())
        
            pygame.display.update()
            clock.tick(60)

            if button.button_clicked() == True:
                enemies = pygame.sprite.Group()
                enemy_count = 0
                
                game_over = False



class Button():
    def __init__(self, butx, buty, butwid, buthigh, butcolor, buttext, buttxtcolor, textpadding):
        self.butx = 0
        self.buty = 200
        self.butwid = 40
        self.buthigh = 600
        self.butcolor = "maroon"
        self.buttext = 'the enemies got past you! click to retry'
        self.buttxtcolor = "yellow"
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