from pygame import *
WIDTH = 300
HEIGHT = 250
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock()
running = True
while running:
    clock.tick(FPS)

