from pygame.locals import *
import pygame
from helpers.spritesheet import SpriteSheet
import sys
import os
from colorize import *

script_dir = sys.path[0]

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

dir = os.path.join(script_dir, "../graphics/")

img_path = os.path.join(dir, "extra.png")

graphic = pygame.image.load(img_path).convert_alpha()


pygame.display.set_caption("color test")

i = 0
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    i += 1
    graphic = Colorize.change(graphic, (i % 255, (i / 3) % 255, (i / 6) % 255))

    screen.blit(graphic, (50, 50))
    pygame.display.update()

pygame.quit()
sys.exit()
