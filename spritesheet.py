import pygame
import sys

# import os
# script_dir = sys.path[0]


class SpriteSheet:
    """extract frames from a single spritesheet png, optionally colorize each frame
    :img_path - path to sprite sheet
    """

    def __init__(
        self, img_path, width, height, frame_count, scale=1.0, bg_color=(0, 0, 0, 0)
    ):
        # load sprite sheet
        self.sprite_sheet = pygame.image.load(img_path).convert_alpha()
        # print("sprite post convert to alpha")
        # print(self.sprite_sheet.get_at((0, 0)))
        self.width = width
        self.height = height

        # create frames list
        self.frame_count = frame_count
        self.frames = []
        self.last_update = pygame.time.get_ticks()

        # print(type(self.sprite_sheet))
        for i in range(self.frame_count):
            self.frames.append(self.get_frame(i, scale, bg_color))

    def get_frame(self, frame_num, scale=1.0, color=(0, 0, 0, 0)):
        """retrieve a single frame from a spritesheet, with optional scaling and background coloring"""
        frame = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA
        ).convert_alpha()
        # frame = pygame.Surface((self.width, self.height)).convert_alpha()
        # print("1")
        # print(frame.get_at((0, 0)))
        # frame.set_colorkey(color)
        # print("2")
        # print(frame.get_at((0, 0)))
        x = frame_num * self.width
        y = 0
        frame.blit(
            self.sprite_sheet,
            (0, 0),
            (x, y, self.width, self.height),
        )
        frame = pygame.transform.scale_by(frame, scale).convert_alpha()
        # frame.set_colorkey(color)
        # print("3")
        # print(frame.get_at((0, 0)))
        return frame

    def colorize(self, surface: pygame.Surface, newColor):
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).
        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        # image = self.image.copy()

        # zero out RGB values
        surface.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        surface.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

        return surface

    def fill(self, surface: pygame.Surface, color):
        """Fill all pixels of the surface with color, preserve transparency."""
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))

        return surface
