import pygame
from random import choice, randint


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        dim = choice(range(20, 100))
        speed = 10*(100-dim)/100 + 2
        self.image = pygame.Surface((dim, dim))
        self.image.fill('gray')
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.height_y_constraint = screen_height

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()
