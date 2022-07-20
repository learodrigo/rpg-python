import pygame

from csv import reader
from os import walk
from typing import List


def import_csv_layout(path: str) -> list:
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map


def import_folder(path: str) -> List[pygame.Surface]:
    surfaces = []
    for _, __, img_files in walk(path):
        for img in sorted(img_files):
            full_path = f"{path}/{img}"
            image_surface = pygame.image.load(full_path).convert_alpha()
            surfaces.append(image_surface)
    return surfaces
