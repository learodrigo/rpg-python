from secrets import choice
import pygame
from particle import ParticleEffect

from support import import_folder
from typing import List, Tuple

from y_sort_camera_group import YSortCameraGroup


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # Magic
            "flame": [import_folder("graphics/particles/flame/frames")],
            "aura": [import_folder("graphics/particles/aura")],
            "heal": [import_folder("graphics/particles/heal/frames")],
            # Attacks
            "claw": [import_folder("graphics/particles/claw")],
            "slash": [import_folder("graphics/particles/slash")],
            "sparkle": [import_folder("graphics/particles/sparkle")],
            "leaf_attack": [import_folder("graphics/particles/leaf_attack")],
            "thunder": [import_folder("graphics/particles/thunder")],
            # Monste deaths
            "squid": [import_folder("graphics/particles/smoke_orange")],
            "raccoon": [import_folder("graphics/particles/raccoon")],
            "spirit": [import_folder("graphics/particles/nova")],
            "bamboo": [import_folder("graphics/particles/bamboo")],
            # Leafs
            "leaf": [
                import_folder("graphics/particles/leaf1"),
                import_folder("graphics/particles/leaf2"),
                import_folder("graphics/particles/leaf3"),
                import_folder("graphics/particles/leaf4"),
                import_folder("graphics/particles/leaf5"),
                import_folder("graphics/particles/leaf6"),
                self.reflect_images(import_folder("graphics/particles/leaf1")),
                self.reflect_images(import_folder("graphics/particles/leaf2")),
                self.reflect_images(import_folder("graphics/particles/leaf3")),
                self.reflect_images(import_folder("graphics/particles/leaf4")),
                self.reflect_images(import_folder("graphics/particles/leaf5")),
                self.reflect_images(import_folder("graphics/particles/leaf6")),
            ],
        }

    def reflect_images(self, frames: List[pygame.Surface]) -> List[pygame.Surface]:
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, flip_x=True, flip_y=False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_particles(
        self,
        animation_type: str,
        groups: List[YSortCameraGroup],
        pos: Tuple,
    ):
        animation_frames = choice(self.frames[animation_type])
        ParticleEffect(animation_frames=animation_frames, groups=groups, pos=pos)
