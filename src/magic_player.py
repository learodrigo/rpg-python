import pygame

from animation_player import AnimationPlayer
from player import Player
from random import randint
from settings import *
from typing import List
from y_sort_camera_group import YSortCameraGroup


class MagicPlayer:
    def __init__(self, animation_player: AnimationPlayer):
        self.animation_player = animation_player
        self.sounds = {
            "heal": pygame.mixer.Sound("audio/heal.wav"),
            "flame": pygame.mixer.Sound("audio/Fire.wav"),
        }

    def heal(
        self,
        cost: float,
        groups: List[YSortCameraGroup],
        player: Player,
        strength: float,
    ):
        if player.energy >= cost:
            self.sounds["heal"].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            self.animation_player.create_particles(
                animation_type="aura",
                groups=groups,
                pos=player.rect.center,
            )
            self.animation_player.create_particles(
                animation_type="heal",
                groups=groups,
                pos=player.rect.center + pygame.math.Vector2(0, -60),
            )

    def flame(
        self,
        cost: float,
        groups: List[YSortCameraGroup],
        player: Player,
    ):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds["flame"].play()

            if player.status.split("_")[0] == "up":
                direction = pygame.math.Vector2(0, -1)
            elif player.status.split("_")[0] == "right":
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split("_")[0] == "down":
                direction = pygame.math.Vector2(0, 1)
            elif player.status.split("_")[0] == "left":
                direction = pygame.math.Vector2(-1, 0)

            for i in range(1, 6):
                if direction.x:
                    offset_x = (direction.x * i) * TILESIZE
                    x = (
                        player.rect.centerx
                        + offset_x
                        + randint(-TILESIZE // 3, TILESIZE // 3)
                    )
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles(
                        animation_type="flame",
                        pos=(x, y),
                        groups=groups,
                    )
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = (
                        player.rect.centery
                        + offset_y
                        + randint(-TILESIZE // 3, TILESIZE // 3)
                    )
                    self.animation_player.create_particles(
                        animation_type="flame",
                        pos=(x, y),
                        groups=groups,
                    )
