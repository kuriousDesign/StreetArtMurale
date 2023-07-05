import pygame
from helpers.spritesheet import *
from typing import List
from clipplayer import *


class WaterClipNames(enumerate):
    LOOP = 0


class Water:
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
        LOOP = 0
        """

        clips: List[ClipData] = list()

        path = "assets/images/water/spritesheet_water_W3840H2160F4.png"
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

        return clips
