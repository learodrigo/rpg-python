import pygame
from player import Player

from settings import (
    BAR_COLOR,
    BAR_COLOR_SELECTED,
    TEXT_COLOR,
    TEXT_COLOR_SELECTED,
    UI_BG_COLOR,
    UI_BORDER_COLOR,
    UPGRADE_BG_COLOR_SELECTED,
)


class UpgradeItem:
    def __init__(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        index: int,
        font: pygame.font.Font,
    ):
        self.rect = pygame.Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display_name(
        self,
        surface: pygame.Surface,
        name: str,
        cost: float,
        selected: bool,
    ):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        title_surface = self.font.render(name, False, color)
        title_rect = title_surface.get_rect(
            midtop=self.rect.midtop + pygame.math.Vector2(0, 20)
        )

        cost_surface = self.font.render(str(int(cost)), False, color)
        cost_rect = cost_surface.get_rect(
            midbottom=self.rect.midbottom - pygame.math.Vector2(0, 20)
        )

        surface.blit(title_surface, title_rect)
        surface.blit(cost_surface, cost_rect)

    def display_bar(
        self,
        surface: pygame.Surface,
        value: int,
        max_value: int,
        selected: bool,
    ):
        top = self.rect.midtop + pygame.math.Vector2(0, 60)
        bottom = self.rect.midbottom - pygame.math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        full_height = bottom[1] - top[1]
        relative_height = (value / max_value) * full_height
        width = 30
        value_rect = pygame.Rect(
            top[0] - width / 2,
            bottom[1] - relative_height,
            width,
            10,
        )

        pygame.draw.line(surface, color, top, bottom, 5)
        pygame.draw.rect(surface, color, value_rect)

    def trigger(self, player: Player):
        upgrade_attribute = list(player.stats.keys())[self.index]

        if (
            player.exp >= player.upgrade_cost[upgrade_attribute]
            and player.stats[upgrade_attribute] < player.max_stats[upgrade_attribute]
        ):
            player.exp -= player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute] *= 1.2
            player.upgrade_cost[upgrade_attribute] *= 1.4

        if player.stats[upgrade_attribute] > player.max_stats[upgrade_attribute]:
            player.stats[upgrade_attribute] = player.max_stats[upgrade_attribute]

    def display(
        self,
        surface: pygame.Surface,
        select_number: int,
        name: str,
        value: int,
        max_value: int,
        cost: int,
    ):
        is_selected = self.index == select_number
        if is_selected:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect, 4)

        self.display_name(
            cost=cost,
            name=name,
            surface=surface,
            selected=is_selected,
        )
        self.display_bar(
            surface=surface,
            value=value,
            max_value=max_value,
            selected=is_selected,
        )
