import pygame

from player import Player
from settings import UI_FONT, UI_FONT_SIZE
from upgrade_item import UpgradeItem


class Upgrade:
    def __init__(self, player: Player):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.attribute_number = len(player.stats)
        self.attribute_names = list(player.stats.keys())
        self.max_values = list(player.max_stats.values())
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

        # Items
        self.height = self.display_surface.get_size()[1] * 0.8
        self.width = self.display_surface.get_size()[0] // 6
        self.create_items()

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.attribute_number)):
            full_width = self.display_surface.get_size()[0]
            increment = full_width // self.attribute_number
            left = (item * increment) + (increment - self.width) // 2

            top = self.display_surface.get_size()[1] * 0.1

            item = UpgradeItem(
                left=left,
                top=top,
                width=self.width,
                height=self.height,
                index=index,
                font=self.font,
            )

            self.item_list.append(item)

    def input(self):
        if self.can_move:
            keys = pygame.key.get_pressed()

            if (
                keys[pygame.K_RIGHT]
                and self.selection_index < self.attribute_number - 1
            ):
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index >= 1:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def display(self):
        self.input()
        self.selection_cooldown()

        for index, item in enumerate(self.item_list):
            name = self.attribute_names[index]
            value = self.player.get_value_by_index(index)
            max_value = self.max_values[index]
            cost = self.player.get_cost_by_index(index)

            item.display(
                surface=self.display_surface,
                select_number=self.selection_index,
                name=name,
                value=value,
                max_value=max_value,
                cost=cost,
            )
