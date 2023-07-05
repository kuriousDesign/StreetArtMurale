import pygame
from spritesheet import *
from typing import List
from clipplayer import *


class BirdClipNames(enumerate):
    LEAVING_HOME = 0
    FOLLOWING = 1
    LANDING = 2  # depricated
    KISSING = 3
    GOING_HOME = 4
    UPDOWN = 5


class Bird:
    def __init__(
        self,
    ):
        self._is_visible = True
        # frame kinematics and scaling

        self.scale = 1.0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        self.clip_player = ClipPlayer(self.load_clips())

        self.clip_is_finished = False
        self.rect = pygame.Rect((self.x, self.y, 80, 180))
        self.vel_y = 0

    def set_visibility(self, is_visible):
        self._is_visible = is_visible
        self.clip_player.is_visible = self._is_visible

    def get_visibility(self):
        self._is_visible = self.clip_player.is_visible
        return self._is_visible

    def load_clips(self):
        # create clip list

        """
        LEAVING_HOME = 0
        FOLLOWING = 1
        LANDING = 2
        KISSING = 3
        GOING_HOME = 4
        """

        clips: List[ClipData] = list()

        # LEAVING HOME
        path = "assets/images/bird/spritesheet_bird_leavinghome_F4.png"
        sprite_sheet = SpriteSheet(path, 1920 * 2, 1080 * 2, 4, 0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        # FOLLOWING
        path = "assets/images/bird/bird_flying_W3508H2612_F3.png"
        sprite_sheet = SpriteSheet(path, 3508, 2612, 3, 0.09)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        # LANDING
        path = "assets/images/bird/spritesheet_bird_landing_W456H1528F9.png"
        sprite_sheet = SpriteSheet(path, 456, 1528, 9, 0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        # KISS
        path = "assets/images/bird/spritesheet_bird_kiss_F5.png"
        sprite_sheet = SpriteSheet(path, 1920 * 2, 1080 * 2, 5, 0.5)
        kiss_fx = pygame.mixer.Sound("assets/audio/kiss.wav")
        kiss_fx.set_volume(0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
                kiss_fx,
            )
        )

        # GOING HOME
        path = "assets/images/bird/spritesheet_bird_gohome_F5.png"
        sprite_sheet = SpriteSheet(path, 1920 * 2, 1080 * 2, 4, 0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        # UP DOWN
        path = "assets/images/bird/spritesheet_bird_upanddown_W1920H2289F8.png"
        sprite_sheet = SpriteSheet(path, 1920, 2289, 9, 0.4)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        return clips

    def move(self, type: str, x, y):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        if type.lower() == "relative" or type.lower() == "rel":
            self.x += x
            self.y += y
            print("relative move")
            print(x)
        elif type.lower() == "absolute" or type.lower() == "abs":
            self.x = x
            self.y = y

        self.clip_player.x = self.x
        self.clip_player.y = self.y

    def draw(self, screen):
        self.clip_player.draw(screen, self.x, self.y)
