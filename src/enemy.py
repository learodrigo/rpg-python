import pygame

from entity import Entity
from player import Player
from settings import *
from support import *
from typing import Callable, List, Tuple
from y_sort_camera_group import YSortCameraGroup


class Enemy(Entity):
    def __init__(
        self,
        add_exp: Callable,
        damage_player: Callable,
        groups: List[YSortCameraGroup],
        monster_name: str,
        obstacle_sprites: pygame.sprite.Group,
        pos: Tuple,
        trigger_death_particles: Callable,
    ):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.monster_name = monster_name

        # Graphics setup
        self.import_graphics(self.monster_name)
        self.status = "idle"
        self.image = self.animations[self.status][self.frame_index]

        # Movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # Stats
        monster_info = MONSTER_DATA[self.monster_name]
        self.attack_radius = monster_info["attack_radius"]
        self.attack_type = monster_info["attack_type"]
        self.damage = monster_info["damage"]
        self.exp = monster_info["exp"]
        self.health = monster_info["health"]
        self.notice_radius = monster_info["notice_radius"]
        self.resistance = monster_info["resistance"]
        self.speed = monster_info["speed"]

        # Player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

        # Vulnerability timer
        self.vulnerable = True
        self.hit_time = None
        self.vulnerability_duration = 300

        # Sound
        self.death_sound = pygame.mixer.Sound("audio/death.wav")
        self.hit_sound = pygame.mixer.Sound("audio/hit.wav")
        self.attack_sound = pygame.mixer.Sound(monster_info["attack_sound"])
        self.death_sound.set_volume(0.6)
        self.hit_sound.set_volume(0.6)
        self.attack_sound.set_volume(0.3)

    def import_graphics(self, name: str):
        self.animations = {
            "idle": [],
            "move": [],
            "attack": [],
        }

        main_path = f"graphics/monsters/{name}"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(f"{main_path}/{animation}")

    def get_player_distance_direction(self, player: Player) -> tuple:
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player: Player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != "attack":
                self.frame_index = 0
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player: Player):
        if self.status == "attack":
            self.attack_sound.play()
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(amount=self.damage, attack_type=self.attack_type)
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player=player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.vulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        alpha = self.wave_value() if not self.vulnerable else 255
        self.image.set_alpha(alpha)

    def get_damage(self, player: Player, attack_type: str):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player=player)[1]

            if attack_type == "weapon":
                self.health -= player.get_full_weapon_damage()
            elif attack_type == "magic":
                self.health -= player.get_magic_damage()

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.trigger_death_particles(
                pos=self.rect.center,
                particle_type=self.monster_name,
            )
            self.add_exp(amount=self.exp)
            self.death_sound.play()
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.hit_reaction()
        self.move(speed=self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player: Player):
        self.get_status(player=player)
        self.actions(player=player)
