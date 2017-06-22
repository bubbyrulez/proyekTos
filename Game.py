#pygame skeleton
#import os
from sprites import *
from settings import *

#initiate and create game window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(game_title)
clock = pygame.time.Clock()

#sprite group
all_sprites = pygame.sprite.Group()
#add sprite to Group
player = Player()
all_sprites.add(player)

#game loop
running = True
while running:
    #keep loop running at right speed
    clock.tick(FPS)
    #process inp (event)
    for event in pygame.event.get():
        #check for x button
        if event.type == pygame.QUIT:
            running = False

    #update
    all_sprites.update()

    #draw or render
    screen.fill(BLUE)
    all_sprites.draw(screen)

    #displaythe rendered
    pygame.display.flip()

pygame.quit()
