import pygame

from player import Player
from typing import List
from y_sort_camera_group import YSortCameraGroup


class Weapon(pygame.sprite.Sprite):
    def __init__(
        self,
        player: Player,
        groups: List[YSortCameraGroup],
    ):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.status.split("_")[0]

        # Graphics
        image_path = f"graphics/weapons/{player.weapon}/{direction}.png"
        self.image = pygame.image.load(image_path).convert_alpha()

        # Placement
        if direction == "left":
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pygame.math.Vector2(0, 16)
            )
        elif direction == "right":
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pygame.math.Vector2(0, 16)
            )
        elif direction == "up":
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0)
            )
        elif direction == "down":
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0)
            )
