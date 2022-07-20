import pygame

from math import sin
from typing import List
from y_sort_camera_group import YSortCameraGroup


class Entity(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: List[YSortCameraGroup],
    ):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed: float):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision(direction="horizontal")
        self.hitbox.y += self.direction.y * speed
        self.collision(direction="vertical")

        self.rect.center = self.hitbox.center

    def collision(self, direction: str):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self) -> int:
        value = sin(pygame.time.get_ticks())
        return 255 if value >= 0 else 0
