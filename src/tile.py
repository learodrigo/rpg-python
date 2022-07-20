import pygame

from settings import *
from typing import List, Tuple
from y_sort_camera_group import YSortCameraGroup


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: Tuple,
        groups: List[YSortCameraGroup],
        sprite_type: str,
        surface=pygame.Surface((TILESIZE, TILESIZE)),
    ):
        super().__init__(groups)
        self.image = surface
        self.sprite_type = sprite_type

        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)

        y_offset = HITBOX_OFFSET[self.sprite_type]
        self.hitbox = self.rect.inflate(0, y_offset)
