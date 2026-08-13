"""
Slime Shooterz - Game Constants
Developed by MANBOY
"""

import os
import sys

# Helper function to get resource path (works for both dev and compiled EXE)
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Slime Shooterz"
FPS = 60

# Colors (Slime Theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
GREEN = (50, 205, 50)
DARK_GREEN = (0, 100, 0)
LIME = (50, 205, 50)
NEON_GREEN = (57, 255, 20)
SLIME_GREEN = (136, 255, 0)
DARK_SLIME = (0, 80, 0)
PURPLE = (180, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 215, 0)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)
DARK_GOLD = (80, 60, 0)

# Asset Paths - Using get_resource_path for all assets
ASSETS_PATH = get_resource_path("assets/")
IMAGES_PATH = get_resource_path("assets/images/")
SOUNDS_PATH = get_resource_path("assets/sounds/")

# Logo path
LOGO_PATH = get_resource_path("logo.png")
LOGO_PATH_ALT = get_resource_path("assets/logo.png")

# Image files
PLAYER_IMAGE = get_resource_path("assets/images/player/player_ship_blue.png")
PLAYER_IMAGE_ALT = get_resource_path("assets/images/player/player_ship_red.png")
EASY_ENEMY_IMAGE = get_resource_path("assets/images/enemies/easy_enemy_orange.png")
BOSS_ENEMY_IMAGE_1 = get_resource_path("assets/images/enemies/boss_enemy_green.png")
BOSS_ENEMY_IMAGE_2 = get_resource_path("assets/images/enemies/boss_enemy_purple.png")
PLAYER_BULLET_IMAGE = get_resource_path("assets/images/bullets/player_laser_blue.png")
BOSS_BULLET_IMAGE = get_resource_path("assets/images/bullets/boss_laser_red.png")
POWERUP_IMAGE = get_resource_path("assets/images/powerup.png")

# Sound files
GUN_SOUND = get_resource_path("assets/sounds/gun_shot.wav")
ENEMY_DEATH_SOUND = get_resource_path("assets/sounds/enemy_death.wav")
BOSS_EXPLOSION_SOUND = get_resource_path("assets/sounds/boss_explosion.wav")
BOSS_SHOT_SOUND = get_resource_path("assets/sounds/boss_shot.wav")
PLAYER_HIT_SOUND = get_resource_path("assets/sounds/player_hit.wav")
GAME_OVER_SOUND = get_resource_path("assets/sounds/game_over.wav")
ENEMY_SHOOT_SOUND = get_resource_path("assets/sounds/enemy_shot.wav")
POWERUP_SOUND = get_resource_path("assets/sounds/powerup.wav")
BOSS_WARNING_SOUND = get_resource_path("assets/sounds/boss_warning.wav")
BACKGROUND_MUSIC = get_resource_path("assets/sounds/background_music.wav")

# Player
PLAYER_SPEED = 5
PLAYER_START_X = SCREEN_WIDTH // 2
PLAYER_START_Y = SCREEN_HEIGHT - 100
INITIAL_LIVES = 3
PLAYER_SIZE = 30
PLAYER_INVINCIBILITY_TIME = 60

# Easy Enemy (Alien)
EASY_ENEMY_SPEED_MIN = 1.5
EASY_ENEMY_SPEED_MAX = 3
EASY_ENEMY_SPAWN_RATE = 60
MAX_EASY_ENEMIES = 8
EASY_ENEMY_SIZE = 25
EASY_ENEMY_HEALTH = 1
EASY_ENEMY_POINTS = 10
EASY_ENEMY_SHOOT_RATE = 120
ENEMY_BULLET_SPEED = 3

# Boss Enemy - 3 Alien types
BOSS_TYPES = [
    {'name': 'Slime King', 'health': 20, 'speed': 1.5, 'size': 45, 'points': 100, 'shoot_rate': 90, 'color': LIME},
    {'name': 'Alien Queen', 'health': 30, 'speed': 2.0, 'size': 50, 'points': 150, 'shoot_rate': 70, 'color': PURPLE},
    {'name': 'Cosmic Slime', 'health': 40, 'speed': 2.5, 'size': 55, 'points': 200, 'shoot_rate': 50, 'color': NEON_GREEN}
]

BOSS_SPAWN_SCORE = 50
BOSS_WARNING_DURATION = 120
BOSS_BULLET_SPEED = 4

# Bullets
PLAYER_BULLET_SPEED = 7
PLAYER_BULLET_SIZE = 5
BOSS_BULLET_SIZE = 8
ENEMY_BULLET_SIZE = 5
MAX_PLAYER_BULLETS = 30
MAX_BOSS_BULLETS = 15
MAX_ENEMY_BULLETS = 20

# Power-up System
POWERUP_DROP_CHANCE = 0.15
POWERUP_DURATION = 600
POWERUP_SIZE = 20
POWERUP_BULLET_SPEED = 10
MAX_POWERUP_BULLETS = 50

# Stars
STAR_COUNT = 100
STAR_SPEED_MIN = 0.5
STAR_SPEED_MAX = 2.5
STAR_SIZE_MIN = 1
STAR_SIZE_MAX = 3

# UI
UI_FONT_SIZE = 36
GAME_OVER_FONT_SIZE = 64
UI_PADDING = 10
BOSS_HEALTH_BAR_WIDTH = 300
BOSS_HEALTH_BAR_HEIGHT = 20
BOSS_HEALTH_BAR_Y = 20

# Developer Credit
DEVELOPER = "Developed by MANBOY"