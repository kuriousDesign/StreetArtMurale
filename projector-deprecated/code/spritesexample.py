from colorize import *
import pygame
from spritesheet import SpriteSheet
import sys
import os

script_dir = sys.path[0]
graphics_dir = os.path.join(script_dir, "../graphics/")
spritesheets_dir = os.path.join(script_dir, "../graphics/spritesheets/")

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Spritesheets")

sprite_img_path = os.path.join(spritesheets_dir, "bird_flying_W3508H2612.png")

# sprite_img_path = "/home/jake/repos/StreetArtMurale/projector/graphics/spritesheets/bird_flying _W3508H2612.png"
# bird_img_path = os.path.join(script_dir, '../graphics/image_bird.png')
# sprite_sheet_image = pygame.image.load(sprite_img_path).convert_alpha()
# bird_image = pygame.image.load(bird_img_path).convert_alpha()

BG = (20, 20, 20)
BLACK = (0, 0, 0)

ww = 3508
hh = 2612
sprite_sheet = SpriteSheet(sprite_img_path, ww, hh, 3, 100)


########################################################################################
# LOAD GRAPHICS

img_path = os.path.join(graphics_dir, "scene_base.png")

img = pygame.image.load(img_path).convert_alpha()
scene_base = pygame.transform.scale_by(img, 0.5)
img_path = os.path.join(graphics_dir, "waterfall_colorize.png")
img = pygame.image.load(img_path).convert_alpha()
waterfall_colorize = pygame.transform.scale_by(img, 0.5)


# SPRITE SHEETS


###########################################################################################


last_update = pygame.time.get_ticks()
x_pos = 0
x_dir = 1
x_step = 30

animation_cooldown = 100
animation_steps = 3
animation_list = []

frame = 0

for i in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(i, 0.1, (0, 0, 0)))


run = True
i = 0
while run:
    i += 1
    # update background
    screen.fill(BG)

    # base layer of the scene
    screen.blit(scene_base, (0, 0))

    # colorize layers
    waterfall_colorize = Colorize.apply_color(
        waterfall_colorize, (255 - i % 255, 255 - (i / 3) % 255, (i / 6) % 255)
    )
    screen.blit(waterfall_colorize, (0, 0))

    # update bird animation
    current_time = pygame.time.get_ticks()

    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        x_pos += x_step * x_dir
        if frame >= animation_steps:
            frame = 0

        show_frame = animation_list[frame]
        # show_frame = pygame.transform.scale_by(show_frame, abs((x_pos+50)/(SCREEN_WIDTH+50)))
        if x_pos > SCREEN_WIDTH - 150:
            x_dir = -1
            x_pos += x_step * x_dir
        elif x_pos < 0:
            x_dir = 1
            x_pos += x_step * x_dir

        if x_dir < 0:
            show_frame = pygame.transform.flip(show_frame, True, False)
            # show_frame.set_colorkey((0, 0, 0))

    # show frame image
    screen.blit(show_frame, (x_pos, 0))
    # screen.blit(frame_3, (250, 0))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
