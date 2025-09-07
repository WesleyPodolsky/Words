import pygame
pygame.init()
from pathlib import Path
images = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
assets = Path(__file__).parent / "images"



screen = pygame.display.set_mode((640, 480))

class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()

            self.image = pygame.Surface((10, 10))
            self.rect = self.image.get_rect()
            self.rect.x = 100
            self.rect.y = 100



            self.player = pygame.image.load("/workspaces/Words/lessons/07_Projects/04_Asteroids/images/ship.png")
            self.image = self.player
            self.image = pygame.transform.scale(self.image, (50, 50))
            self.rect = self.image.get_rect(center=self.rect.center)



            
player = Player()
player_group = pygame.sprite.GroupSingle(player)




def main():

    player = Player()
    player_group.add(player)
    
    while True:
        screen.fill("red")
        player_group.draw(screen)

   


    



   
    


if __name__ == "__main__":
    main()