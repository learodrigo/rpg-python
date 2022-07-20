import pygame

from animation_player import AnimationPlayer
from enemy import Enemy
from magic_player import MagicPlayer
from player import Player
from random import choice, randint
from support import import_csv_layout, import_folder
from settings import *
from tile import Tile
from typing import Tuple
from ui import UI
from upgrade import Upgrade
from weapon import Weapon
from y_sort_camera_group import YSortCameraGroup


class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Sprint set up
        self.create_map()

        # Attack sprites
        self.current_attack = None

        # User interface
        self.ui = UI()
        self.upgrade = Upgrade(player=self.player)

        # Particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(animation_player=self.animation_player)

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def create_map(self):
        layouts = {
            "boundary": import_csv_layout("map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("map/map_Grass.csv"),
            "object": import_csv_layout("map/map_Objects.csv"),
            "entities": import_csv_layout("map/map_Entities.csv"),
        }

        graphics = {
            "grass": import_folder("graphics/grass"),
            "object": import_folder("graphics/objects"),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                y = row_index * TILESIZE
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        pos = (x, y)

                        if style == "boundary":
                            Tile(
                                groups=[self.obstacle_sprites],
                                pos=pos,
                                sprite_type="invisible",
                            )
                        if style == "grass":
                            random_grass = choice(graphics[style])
                            Tile(
                                groups=[
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites,
                                ],
                                pos=pos,
                                sprite_type=style,
                                surface=random_grass,
                            )
                        if style == "object":
                            surface = graphics[style][int(col)]
                            Tile(
                                groups=[self.visible_sprites, self.obstacle_sprites],
                                pos=pos,
                                sprite_type=style,
                                surface=surface,
                            )
                        if style == "entities":
                            # Player
                            if col == "394":
                                self.player = Player(
                                    create_attack=self.create_attack,
                                    create_magic=self.create_magic,
                                    destroy_attack=self.destroy_attack,
                                    groups=[self.visible_sprites],
                                    pos=pos,
                                    obstacle_sprites=self.obstacle_sprites,
                                )
                            else:
                                if col == "390":
                                    monster_name = "bamboo"
                                elif col == "391":
                                    monster_name = "spirit"
                                elif col == "392":
                                    monster_name = "raccoon"
                                else:
                                    monster_name = "squid"

                                Enemy(
                                    add_exp=self.add_exp,
                                    damage_player=self.damage_player,
                                    groups=[
                                        self.visible_sprites,
                                        self.attackable_sprites,
                                    ],
                                    monster_name=monster_name,
                                    obstacle_sprites=self.obstacle_sprites,
                                    pos=pos,
                                    trigger_death_particles=self.trigger_death_particles,
                                )

    def create_attack(self):
        self.current_attack = Weapon(
            player=self.player,
            groups=[self.visible_sprites, self.attack_sprites],
        )

    def create_magic(self, style: str, strength: int, cost: int):
        if style == "heal":
            self.magic_player.heal(
                cost=cost,
                groups=[self.visible_sprites],
                player=self.player,
                strength=strength,
            )
        elif style == "flame":
            self.magic_player.flame(
                cost=cost,
                groups=[self.visible_sprites, self.attack_sprites],
                player=self.player,
            )

    def destroy_attack(self):
        if self.current_attack is not None:
            self.current_attack.kill()
            self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    sprite=attack_sprite,
                    group=self.attackable_sprites,
                    dokill=False,
                )

                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for _ in range(randint(3, 7)):
                                self.animation_player.create_particles(
                                    pos=pos - offset,
                                    groups=[self.visible_sprites],
                                    animation_type="leaf",
                                )
                            target_sprite.kill()
                        elif target_sprite.sprite_type == "enemy":
                            target_sprite.get_damage(
                                player=self.player,
                                attack_type=attack_sprite.sprite_type,
                            )

    def damage_player(self, amount: int, attack_type: str):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(
                animation_type=attack_type,
                groups=[self.visible_sprites],
                pos=self.player.rect.center,
            )

    def trigger_death_particles(self, pos: Tuple, particle_type: str):
        self.animation_player.create_particles(
            animation_type=particle_type,
            groups=self.visible_sprites,
            pos=pos,
        )

    def add_exp(self, amount: int):
        self.player.exp += amount

    def run(self):
        self.visible_sprites.custom_draw(player=self.player)
        self.ui.display(player=self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
