import pygame

from entity import Entity
from settings import *
from support import import_folder
from typing import Callable, List, Tuple
from y_sort_camera_group import YSortCameraGroup


class Player(Entity):
    def __init__(
        self,
        pos: Tuple,
        groups: List[YSortCameraGroup],
        obstacle_sprites: pygame.sprite.Group,
        create_attack: Callable,
        destroy_attack: Callable,
        create_magic: Callable,
    ):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-12, HITBOX_OFFSET["player"])

        # Graphics setup
        self.import_player_assets()
        self.status = "down"

        # Movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # Weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = self.get_weapon_name(self.weapon_index)
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = self.get_magic(self.magic_index)
        self.can_switch_magic = True
        self.magic_switch_time = None

        # Stats
        self.stats = PLAYER_STATS.copy()
        self.max_stats = MAX_STATS.copy()
        self.upgrade_cost = UPGRADE_COST.copy()
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.exp = 100

        # Damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.vulnerability_duration = 500

        # Sounds
        self.weapon_attack_sound = pygame.mixer.Sound("audio/sword.wav")
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self):
        character_path = "graphics/player"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_attack": [],
            "down_attack": [],
            "left_attack": [],
            "right_attack": [],
        }

        for animation in self.animations.keys():
            full_path = f"{character_path}/{animation}"
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "_idle" in self.status and not "_attack" in self.status:
                self.status += "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "_attack" in self.status:
                if "_idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status += "_attack"
        else:
            if "_attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Movement input vertical
            if keys[pygame.K_UP]:
                self.status = "up"
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.status = "down"
                self.direction.y = 1
            else:
                self.direction.y = 0

            # Movement input horizontal
            if keys[pygame.K_LEFT]:
                self.status = "left"
                self.direction.x = -1
            elif keys[pygame.K_RIGHT]:
                self.status = "right"
                self.direction.x = 1
            else:
                self.direction.x = 0

            # Attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(WEAPON_DATA.keys()) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = self.get_weapon_name(self.weapon_index)

            # Magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = self.magic
                strength = (
                    self.get_magic_object(self.magic)["strength"] + self.stats["magic"]
                )
                cost = self.get_magic_object(self.magic)["cost"]
                self.create_magic(style=style, strength=strength, cost=cost)

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                if self.magic_index < len(MAGIC_DATA.keys()) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = self.get_magic(self.magic_index)

    def get_weapon_name(self, index: int) -> str:
        return list(WEAPON_DATA.keys())[index]

    def get_magic(self, index: int) -> str:
        return list(MAGIC_DATA.keys())[index]

    def get_full_weapon_damage(self) -> int:
        return self.stats["attack"] + self.get_weapon_object(self.weapon)["damage"]

    def get_magic_damage(self) -> int:
        return self.stats["magic"] + MAGIC_DATA[self.magic]["strength"]

    def get_weapon_object(self, weapon: str) -> dict:
        return WEAPON_DATA[weapon]

    def get_magic_object(self, magic: str) -> dict:
        return MAGIC_DATA[magic]

    def get_value_by_index(self, index: int) -> int:
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index: int) -> int:
        return list(self.upgrade_cost.values())[index]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if (
                current_time - self.attack_time
                >= self.attack_cooldown
                + self.get_weapon_object(self.weapon)["cooldown"]
            ):
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.vulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        alpha = self.wave_value() if not self.vulnerable else 255
        self.image.set_alpha(alpha)

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.energy_recovery()
