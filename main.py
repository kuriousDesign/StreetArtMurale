import pygame
from pygame import mixer

# from fighter import Fighter
from objects.bird import *
from objects.water import *
from objects.gato import *
import os
from colorize import *
import itertools
from colorfade import *

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class ProjectorGame:
    # set framerate
    clock = pygame.time.Clock()
    FPS = 60
    draw_cooldown = 1000.0 / FPS
    last_draw_time = 0

    # event checking
    last_event_check_time = 0
    event_check_cooldown = 5

    # define colours
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        # load music
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.005)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
        magic_fx.set_volume(0.05)

        # replace color in image
        def color_replace(image, search_color, replace_color):
            pygame.transform.threshold(
                image, image, search_color, (0, 0, 0, 0), replace_color, 1, None, True
            )
            return image

    # this is commented out, please import colorize
    """
        # function for colorizing images
        def colorize(image, newColor):
            ""
            Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
            original).
            :param image: Surface to create a colorized copy of
            :param newColor: RGB color to use (original alpha values are preserved)
            :return: New colorized Surface instance
            ""
            # image = self.image.copy()

            # zero out RGB values
            image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
            # add in new RGB values
            image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

            return image
        """

    # load background images

    def create_img_list_from_dir(directory):
        img_list = []
        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                # print(f)
                img_list.append(pygame.image.load(f))

        return img_list

    def merge_img_list(img_list):
        """merge images in list to single flat image"""
        # merge images
        merge_img = None
        for img in img_list:
            if merge_img == None:
                merge_img = img
            else:
                merge_img.blit(img, (0, 0))

        return merge_img

    def load_bg_images():
        merged = None

        # assign directory
        directory = "assets/images/background/"
        # iterate over files in
        # this directory
        # create list of images to be merged
        img_list = create_img_list_from_dir(directory)
        merge_img = merge_img_list(img_list)

        # assign directory
        directory = "assets/images/background/outlines/"
        # iterate over files in
        # the outlines directory
        img_list = create_img_list_from_dir(directory)
        outline_merged = merge_img_list(img_list)

        # colorize the outline merged image to be some new color
        new_color = (0, 0, 0)
        outline_merged = Colorize.change_color(outline_merged, new_color)

        # merge outline into merged
        merge_img.blit(outline_merged, (0, 0))
        img = pygame.transform.scale(merge_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return img.convert_alpha()

    # function for drawing background
    def draw_bg():
        # scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) #removed because it was taking a long time to redraw
        screen.fill((100, 100, 100))
        screen.blit(bg_image, (0, 0))

    # define font
    count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
    score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

    # function for drawing text

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    # function for drawing fighter health bars

    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

    # create instance of objects
    bird = Bird()
    water = Water()
    gato = Gato()

    # colorfade background objects
    img = pygame.image.load("assets/images/background/colorfade/bg_water_color.PNG")
    img1 = pygame.image.load("assets/images/background/colorfade/bg_water_color.PNG")
    img2 = pygame.image.load(
        "assets/images/background/colorfade/bg_lowersplash_color.PNG"
    )
    img.blit(img1, (0, 0))
    img.blit(img2, (0, 0))
    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    colors = itertools.cycle(["blue", "purple", "pink"])
    water_bg = ColorFade(img, colors, FPS, 2000)

    img = pygame.image.load(
        "assets/images/background/colorfade/bg_ladyhair_color.PNG"
    ).convert_alpha()
    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    colors = itertools.cycle(["blue", "red", "pink", "orange"])
    ladyhair_bg = ColorFade(img, colors, FPS, 1000)

    # water_bg.update()
    # ladyhair_bg.update()

    # game setup - execute once at beginning
    bg_image = load_bg_images()
    pygame.display.set_caption("StreetArtMurale")

    # game loop
    run = True
    first_scan = True
    while run:
        current_time = pygame.time.get_ticks()

        # DISPLAY DRAW AT 60 FRAMES PER SECOND
        if current_time - last_draw_time >= draw_cooldown or first_scan:
            clock.tick()

            last_draw_time = current_time
            actual_fps = clock.get_fps()
            if actual_fps < 0.8 * FPS:
                print(clock.get_fps())

            # update objects
            bird.clip_player.update()
            water.clip_player.update()
            gato.clip_player.update()

            # update background colorfade objects
            # water_bg.update() #TODO: this is very time intensive calc, need to find a way to reduce
            # ladyhair_bg.update()  # TODO: this is very time intensive calc, need to find a way to reduce

            # draw background
            draw_bg()
            draw_text("gon world", score_font, (255, 255, 0), 50, 900)

            # draw background colorfade objects
            # water_bg.draw(screen)  # this goes before water #TODO - this is very time intensive
            # ladyhair_bg.draw(screen) #TODO - this is very time intensive

            # draw foreground objects
            bird.draw(screen)
            water.clip_player.draw(screen)
            gato.clip_player.draw(screen)

            # update display - call last
            pygame.display.update()

        # responsive event handler
        if current_time - last_event_check_time >= event_check_cooldown or first_scan:
            last_event_check_time = current_time

            if first_scan:  # initializing routine
                water.clip_player.start_clip(WaterClipNames.LOOP, loop=True)

            # TRANSITIONS
            if bird.clip_player.clip_is_finished:
                match bird.clip_player.active_clip_index:
                    case int(BirdClipNames.LEAVING_HOME):
                        bird.move("absolute", 600, 120)
                        bird.clip_player.start_clip(
                            BirdClipNames.FOLLOWING,
                            loop=True,
                            flip=False,
                        )
                    case int(BirdClipNames.UPDOWN):
                        # bird.move("absolute", 600, 120)
                        if not bird.clip_player.play_in_reverse:
                            bird.move("relative", 250, 0)
                            bird.clip_player.start_clip(
                                BirdClipNames.FOLLOWING,
                                loop=True,
                                flip=bird.clip_player.flip,
                            )
                    case _:
                        pass

                bird.clip_player.clip_is_finished = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        bird.move("absolute", 0, 0)
                        bird.clip_player.start_clip(
                            BirdClipNames.GOING_HOME, loop=False, play_in_reverse=False
                        )

                    elif event.key == pygame.K_h:
                        bird.move("absolute", 0, 0)
                        bird.clip_player.start_clip(
                            BirdClipNames.LEAVING_HOME,
                            loop=False,
                            play_in_reverse=False,
                        )

                    elif event.key == pygame.K_LEFT:
                        bird.clip_player.flip = True
                        bird.move("relative", -30, 0)
                        """
                            bird.clip_player.start_clip(
                                BirdClipNames.FOLLOWING,
                                loop=True,
                                play_in_reverse=True,
                                flip=True,
                            )
                            """
                        print("keydown left arrow")

                    elif event.key == pygame.K_RIGHT:
                        bird.clip_player.flip = False
                        bird.move("relative", 30, 0)
                        """
                            bird.clip_player.start_clip(
                                BirdClipNames.FOLLOWING,
                                loop=True,
                                play_in_reverse=False,
                                flip=False,
                            )
                            """
                        print("keydown right arrow")

                    elif event.key == pygame.K_DOWN:
                        bird.move("relative", -200, 0)
                        bird.clip_player.start_clip(
                            BirdClipNames.UPDOWN,
                            hold_final_frame=True,
                            play_in_reverse=True,
                            flip=bird.clip_player.flip,
                        )
                        print("keydown down arrow")

                    elif event.key == pygame.K_UP:
                        bird.clip_player.start_clip(
                            BirdClipNames.UPDOWN,
                            hold_final_frame=False,
                            play_in_reverse=False,
                            flip=bird.clip_player.flip,
                        )
                        print("keydown up arrow")

                    elif event.key == pygame.K_k:
                        bird.move("absolute", 0, 0)
                        bird.clip_player.start_clip(
                            BirdClipNames.KISSING, loop=False, hold_final_frame=True
                        )
                        print("keydown k")

                    elif event.key == pygame.K_c:
                        gato.move("absolute", 0, 0)
                        gato.clip_player.start_clip(
                            GatoClipNames.WALK, loop=False, hold_final_frame=True
                        )
                        print("keydown c")

        first_scan = False

    # exit pygame
    pygame.quit()


if __name__ == "__main__":
    projection_game = ProjectionGame()
    projection_game.run()
