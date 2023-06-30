import pygame
from spritesheet import SpriteSheet
import sys
import os
script_dir = sys.path[0]

pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_img_path = os.path.join(
    script_dir, '../graphics/spritesheet_bird_flying.png')
bird_img_path = os.path.join(script_dir, '../graphics/image_bird.png')
# sprite_sheet_image = pygame.image.load(sprite_img_path).convert_alpha()
# bird_image = pygame.image.load(bird_img_path).convert_alpha()

BG = (0, 0, 0)
BLACK = (0, 0, 0)

ww = 3508
hh = 2612
sprite_sheet = SpriteSheet(sprite_img_path, ww, hh).sprite_sheet

# create animation list
animation_steps = 3
animation_list = []
last_update = pygame.time.get_ticks()
frame = 0
animation_cooldown = 100
x_pos = 0
x_dir = 1
x_step = 30


for i in range(animation_steps):
    animation_list.append(sprite_sheet.get_image(i, .1, BLACK))


run = True
while run:

    # update background
    screen.fill(BG)

    # update animation
    current_time = pygame.time.get_ticks()

    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        x_pos += x_step*x_dir
        if frame >= animation_steps:
            frame = 0

        show_frame = animation_list[frame]
        # show_frame = pygame.transform.scale_by(show_frame, abs((x_pos+50)/(SCREEN_WIDTH+50)))
        if x_pos > SCREEN_WIDTH - 150:
            x_dir = -1
            x_pos += x_step*x_dir
        elif x_pos < 0:
            x_dir = 1
            x_pos += x_step*x_dir

        if x_dir < 0:
            show_frame = pygame.transform.flip(show_frame, True, False)
    # show frame image
    screen.blit(show_frame, (x_pos, 0))
    screen.blit()

    # screen.blit(frame_3, (250, 0))

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
