import pygame
import itertools
import math
from colorize import *

default_colors = itertools.cycle(["green", "blue", "purple", "pink", "red", "orange"])


class ColorFade:
    def __init__(self, img, colors=default_colors, FPS=60, cooldown=3000):
        self.img = img
        self.colors = colors

        self.base_color = next(self.colors)
        self.next_color = next(self.colors)
        self.current_color = self.base_color

        self.FPS = FPS
        self.change_every_x_seconds = cooldown / 1000.0
        self.number_of_steps = math.ceil(self.change_every_x_seconds * FPS)
        print("num of steps colorfade")
        print(self.number_of_steps)
        self.step = 0

        # self.font = pygame.font.SysFont("Arial", 50)

    def update(self):
        self.step += 1
        if self.step < self.number_of_steps:
            # (y-x)/number_of_steps calculates the amount of change per step required to
            # fade one channel of the old color to the new color
            # We multiply it with the current step counter
            self.current_color = [
                x + (((y - x) / self.number_of_steps) * self.step)
                for x, y in zip(
                    pygame.color.Color(self.base_color),
                    pygame.color.Color(self.next_color),
                )
            ]
        else:
            self.step = 1
            self.base_color = self.next_color
            self.next_color = next(self.colors)

        # print("colorfade current color: ")
        # print(self.current_color)
        rgb = (self.current_color[0], self.current_color[1], self.current_color[2])
        self.img = Colorize.change_color(self.img, rgb)

    def draw(self, surface: pygame.Surface, x=0, y=0):
        surface.blit(self.img, (x, y))
