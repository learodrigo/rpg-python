# Setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    "player": -26,
    "object": -40,
    "grass": -10,
    "invisible": 0,
}

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "graphics/font/joystix.ttf"
UI_FONT_SIZE = 18

# General colors
WATER_COLOR = "#71ddde"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#eeeeee"

# UI colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# Upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#eeeeee"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#eeeeee"

# Player stats
PLAYER_STATS = {
    "attack": 10,
    "energy": 60,
    "health": 100,
    "magic": 4,
    "speed": 5,
}

MAX_STATS = {
    "attack": 20,
    "energy": 140,
    "health": 300,
    "magic": 10,
    "speed": 12,
}

UPGRADE_COST = {
    "attack": 100,
    "energy": 100,
    "health": 100,
    "magic": 100,
    "speed": 100,
}

# Weapons
WEAPON_DATA = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": "graphics/weapons/sword/full.png",
    },
    "lance": {
        "cooldown": 400,
        "damage": 30,
        "graphic": "graphics/weapons/lance/full.png",
    },
    "axe": {
        "cooldown": 300,
        "damage": 20,
        "graphic": "graphics/weapons/axe/full.png",
    },
    "rapier": {
        "cooldown": 50,
        "damage": 8,
        "graphic": "graphics/weapons/rapier/full.png",
    },
    "sai": {
        "cooldown": 80,
        "damage": 10,
        "graphic": "graphics/weapons/sai/full.png",
    },
}

# Magic
MAGIC_DATA = {
    "flame": {
        "cost": 20,
        "graphic": "graphics/particles/flame/fire.png",
        "strength": 5,
    },
    "heal": {
        "cost": 10,
        "graphic": "graphics/particles/heal/heal.png",
        "strength": 20,
    },
}

# Enemies
MONSTER_DATA = {
    "squid": {
        "attack_radius": 80,
        "attack_sound": "audio/attack/slash.wav",
        "attack_type": "slash",
        "damage": 20,
        "exp": 100,
        "health": 100,
        "notice_radius": 360,
        "speed": 3,
        "resistance": 3,
    },
    "raccoon": {
        "attack_sound": "audio/attack/claw.wav",
        "attack_radius": 120,
        "attack_type": "claw",
        "damage": 40,
        "exp": 250,
        "health": 300,
        "notice_radius": 400,
        "resistance": 3,
        "speed": 2,
    },
    "spirit": {
        "attack_radius": 60,
        "attack_sound": "audio/attack/fireball.wav",
        "attack_type": "thunder",
        "damage": 8,
        "exp": 110,
        "health": 100,
        "notice_radius": 350,
        "resistance": 3,
        "speed": 4,
    },
    "bamboo": {
        "attack_radius": 50,
        "attack_sound": "audio/attack/slash.wav",
        "attack_type": "leaf_attack",
        "damage": 6,
        "exp": 120,
        "health": 70,
        "notice_radius": 300,
        "resistance": 3,
        "speed": 3,
    },
}
