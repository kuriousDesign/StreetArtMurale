import pygame
import sys
import os
script_dir = sys.path[0]


class SpriteSheet():
    def __init__(self, image):
        self.sprite_sheet = image
        self.width = 0
        self.height = 0

    def __init__(self, img_path, width, height):
        sprite_sheet = pygame.image.load(img_path).convert_alpha()
        self.sprite_sheet = sprite_sheet
        self.width = width
        self.height = height

    def get_image(self, frame, scale, colour):
        width = self.width
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.spritesheet, (0, 0),
                   ((frame * width), 0, self.width, self.height))
        image = pygame.transform.scale(
            image, (width * scale, self.height * scale))
        image.set_colorkey(colour)

        return self
