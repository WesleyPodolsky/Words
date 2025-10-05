import pygame
from pathlib import Path
import random

shootAngle = random.randint(45,300)
game_over = False
vel = 0
vely = 0
gamespeed = 1
score = 0.0000000000000000000000000000000000001
gotScore = False
highScore = 0.0000000000000000000000000000000000001
fuel = 180
displayFuel = ""


FPS = 60

pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
assets = Path(__file__).parent / "images"

# Screen dimensions
WIDTH, HEIGHT = 600, 450
font = pygame.font.SysFont(None, 40)
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
        global gotScore
        global score
        global highScore
        global fuel
        global displayFuel

        if self.rect.y < 100:
                gotScore = False
                score = 0+ 0.00000000000000000001
                if fuel < 180:
                    fuel += 1
        if gotScore == True:
            if fuel < 180:
                    fuel += 1

        if self.rect.y < 310:
            print("falling", random.randint(0,1))
            vely += 0.1
        else:
            self.rect.y = 309
            print("on ground")
            if gotScore == False:
                gotScore = True
                score = (10-vely) - abs(shootAngle/9) + 0.00000000000000000001
                if score > highScore:
                    highScore = score

        displayFuel = ""
        for i in range(round(fuel/3)):
            displayFuel = displayFuel + "|"

            



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
                    
                    if fuel >= 0:
                        fuel -= 0.5
                        shootAngle+=1
                if keys[pygame.K_RIGHT]:
                    

                    if fuel >= 0:
                        fuel -= 0.5
                        shootAngle-=1
                if keys[pygame.K_UP]:
                    if self.rect.y > 50:
                        if fuel >= 0:
                            vely -=0.3
                            fuel -= 1.5
        
                if keys[pygame.K_DOWN]:
                    vely += 0.1
                    fuel += 0.25

                
                    

        if shootAngle > 180:
            shootAngle = -180
        if shootAngle < -180:
            shootAngle = 180
        print(shootAngle)



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
    global displayFuel

    clock = pygame.time.Clock()

    

    # Group for obstacles
 

    
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


                

                





            
        
            # Draw everything
            screen.fill("black")
            

            pygame.draw.rect(screen, 'darkgray', (0, 350, 600, 600))
            pygame.draw.rect(screen, (30,30,30), (0, 0, 600, 100))

            wave_group.draw(screen)
            
            displayHighScore = font.render("highscore: " + (str(highScore))[0]+ (str(highScore))[1]+ (str(highScore))[2]+ (str(highScore))[3], True, "gold")
            if score < 0.5 and score > 0:
                displayscore = font.render("score: 0", True, "grey")
            elif score < 0:
                displayscore = font.render("kaboom!", True, "grey")
            else:
                displayscore = font.render("score: " + (str(score))[0]+ (str(score))[1]+ (str(score))[2]+ (str(score))[3], True, "grey")
            screen.blit(displayscore, (120,50))

            if highScore > 0.5:
                screen.blit(displayHighScore, (300,50))
            else:
                displayHighScore = font.render("highscore: 0", True, "grey")
                screen.blit(displayHighScore, (300,50))
            displayFuelSurface = font.render("fuel: " + displayFuel, True, "red")
            screen.blit(displayFuelSurface, (10,10))


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