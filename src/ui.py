import pygame
from player import Player
from settings import *


class UI:
    def __init__(self) -> None:
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # Convert weapon
        self.weapon_graphics = []
        for w in WEAPON_DATA.values():
            path = w["graphic"]
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # Convert magic
        self.magic_graphics = []
        for m in MAGIC_DATA.values():
            path = m["graphic"]
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic)

    def show_bar(
        self,
        current: int,
        max_amount: int,
        bg_rect: pygame.Surface,
        color: str,
    ):
        # Bar background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Convert stats to px
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # Bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp: float):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3
        )

    def selection_box(self, left: float, top: float, has_switch: bool) -> pygame.Rect:
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        border_color = UI_BORDER_COLOR_ACTIVE if has_switch else UI_BORDER_COLOR
        pygame.draw.rect(self.display_surface, border_color, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon_index: int, has_switch: bool):
        bg_rect = self.selection_box(left=10, top=630, has_switch=has_switch)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surface, weapon_rect)

    def magic_overlay(self, magic_index: int, has_switch: bool):
        bg_rect = self.selection_box(left=80, top=635, has_switch=has_switch)
        magic_surface = self.magic_graphics[magic_index]
        magic_rect = magic_surface.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surface, magic_rect)

    def display(self, player: Player):
        self.show_exp(exp=player.exp)

        # Magic & Weapon
        self.magic_overlay(
            magic_index=player.magic_index,
            has_switch=not player.can_switch_magic,
        )
        self.weapon_overlay(
            weapon_index=player.weapon_index,
            has_switch=not player.can_switch_weapon,
        )

        # Health & Energy bar
        self.show_bar(
            current=player.health,
            max_amount=player.stats["health"],
            bg_rect=self.health_bar_rect,
            color=HEALTH_COLOR,
        )
        self.show_bar(
            current=player.energy,
            max_amount=player.stats["energy"],
            bg_rect=self.energy_bar_rect,
            color=ENERGY_COLOR,
        )
