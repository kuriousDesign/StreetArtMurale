import pygame


class Colorize:
    def change_color(graphic: pygame.Surface, color):
        graphic.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_MAX)
        graphic.fill(
            (color[0], color[1], color[2], 255), special_flags=pygame.BLEND_RGBA_MIN
        )
        return graphic
