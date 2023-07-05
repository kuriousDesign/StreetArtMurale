import pygame
from laser import Laser
import sys
import os
script_dir = sys.path[0]
player_img_path = os.path.join(script_dir, '../graphics/player.png')
laser_wave_path = os.path.join(script_dir, '../audio/laser.wav')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load(
            player_img_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 100
        self.auto_shoot = True
        self.mute_laser = True
        self.trigger_pull = False

        self.stepper_position = pos[0]

        self.lasers = pygame.sprite.Group()

        self.laser_sound = pygame.mixer.Sound(laser_wave_path)
        self.laser_sound.set_volume(0.5)

    def get_input(self):
        """input is the stepper motor position"""
        self.rect.x = self.stepper_position
        if self.trigger_pull or self.auto_shoot and self.ready:
            self.shoot_laser()

    def get_keyboard_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] or self.auto_shoot and self.ready:
            self.shoot_laser()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
        self.ready = False
        self.laser_time = pygame.time.get_ticks()
        if not self.mute_laser:
            self.laser_sound.play()

    def update(self):
        self.get_keyboard_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
