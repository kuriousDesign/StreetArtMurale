import pygame
import sys

# import os
# script_dir = sys.path[0]


class SpriteSheet:
    """retrieve an image frame from a single spritesheet png"""

    def __init__(self, img_path, width, height, steps, cooldown):
        sprite_sheet = pygame.image.load(img_path).convert_alpha()
        self.sprite_sheet = sprite_sheet
        self.width = width
        self.height = height
        self.image = self.get_image(0, 1.0)

        # create animation list
        self.animation_steps = steps
        self.animation_list = []
        self.last_update = pygame.time.get_ticks()
        self.frame = 0
        self.animation_cooldown = cooldown
        x_pos = 0
        x_dir = 1
        x_step = 30

        for i in range(self.animation_steps):
            self.animation_list.append(self.get_image(i, 0.1, (0, 0, 0)))

    def get_image(self, frame_num, scale=1.0, color=(0, 0, 0)):
        """retrieve a single image from a spritesheet, with optional scaling and background coloring"""
        width = self.width
        self.image = pygame.Surface((self.width, self.height)).convert_alpha()
        self.image.blit(
            self.sprite_sheet, (0, 0), ((frame_num * width), 0, self.width, self.height)
        )
        self.image = pygame.transform.scale(
            self.image, (width * scale, self.height * scale)
        )
        # self.image.set_colorkey(color)
        return self.image

    def colorize(self, newColor):
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).
        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        # image = self.image.copy()

        # zero out RGB values
        self.image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        self.image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

        return self.image

    def fill(self, color):
        """Fill all pixels of the surface with color, preserve transparency."""
        surface = self.image
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))

        return surface
