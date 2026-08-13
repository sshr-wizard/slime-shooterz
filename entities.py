"""
Slime Shooterz - Game Entities
Developed by MANBOY
"""

import pygame
import random
import math
import os
from constants import *

class Player:
    """Player ship with power-up system"""
    def __init__(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.lives = INITIAL_LIVES
        self.score = 0
        self.size = PLAYER_SIZE
        self.invincible = False
        self.invincible_timer = 0
        
        # Power-up system
        self.powerup_active = False
        self.powerup_timer = 0
        self.powerup_type = None
        
        # Load image if available - using get_resource_path from constants
        self.image = None
        self.use_image = False
        if os.path.exists(PLAYER_IMAGE):
            try:
                self.image = pygame.image.load(PLAYER_IMAGE)
                self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
                self.use_image = True
                print(f"Loaded player image: {PLAYER_IMAGE}")
            except Exception as e:
                print(f"Failed to load player image: {e}")
        else:
            print(f"Player image not found: {PLAYER_IMAGE}")
        
    def update(self, keys):
        """Update player position based on key input"""
        if self.invincible:
            self.invincible_timer += 1
            if self.invincible_timer >= PLAYER_INVINCIBILITY_TIME:
                self.invincible = False
                self.invincible_timer = 0
        
        # Movement (Arrow keys or WASD)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        # Keep in bounds
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        self.y = max(self.size, min(SCREEN_HEIGHT - self.size, self.y))
        
        # Update power-up timer
        if self.powerup_active:
            self.powerup_timer += 1
            if self.powerup_timer >= POWERUP_DURATION:
                self.powerup_active = False
                self.powerup_timer = 0
                self.powerup_type = None
                print("Power-up expired!")
    
    def activate_powerup(self, powerup_type):
        """Activate a power-up"""
        self.powerup_active = True
        self.powerup_timer = 0
        self.powerup_type = powerup_type
        print(f"Power-up activated: {powerup_type}!")
    
    def hit(self):
        """Handle player being hit"""
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.invincible_timer = 0
            # Lose power-up when hit
            self.powerup_active = False
            self.powerup_timer = 0
            self.powerup_type = None
            return True
        return False
    
    def get_rect(self):
        """Get collision rectangle"""
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class SlimeAlien:
    """Friendly alien that shoots back (we just don't understand them)"""
    def __init__(self):
        self.x = random.randint(30, SCREEN_WIDTH - 30)
        self.y = -30
        self.speed = random.uniform(EASY_ENEMY_SPEED_MIN, EASY_ENEMY_SPEED_MAX)
        self.size = EASY_ENEMY_SIZE
        self.wobble = random.uniform(1, 3)
        self.wobble_offset = random.uniform(0, math.pi * 2)
        self.health = EASY_ENEMY_HEALTH
        self.points = EASY_ENEMY_POINTS
        self.shoot_timer = random.randint(0, EASY_ENEMY_SHOOT_RATE)
        self.shoot_rate = EASY_ENEMY_SHOOT_RATE
        self.slime_pulse = 0
        
        # Load image if available
        self.image = None
        self.use_image = False
        if os.path.exists(EASY_ENEMY_IMAGE):
            try:
                self.image = pygame.image.load(EASY_ENEMY_IMAGE)
                self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
                self.use_image = True
                print(f"Loaded enemy image: {EASY_ENEMY_IMAGE}")
            except Exception as e:
                print(f"Failed to load enemy image: {e}")
        else:
            print(f"Enemy image not found: {EASY_ENEMY_IMAGE}")
        
    def update(self):
        """Move alien with wobble"""
        self.y += self.speed
        self.x += math.sin(self.y / 50 + self.wobble_offset) * self.wobble
        self.slime_pulse += 0.05
        
        # Keep in horizontal bounds
        self.x = max(self.size, min(SCREEN_WIDTH - self.size, self.x))
        
        # Update shoot timer
        self.shoot_timer += 1
        
        # Return True if off screen
        return self.y > SCREEN_HEIGHT + 30
    
    def should_shoot(self):
        """Check if alien should shoot"""
        if self.y > 50 and self.shoot_timer >= self.shoot_rate:
            self.shoot_timer = 0
            return True
        return False
    
    def take_damage(self, damage=1):
        """Reduce health and return True if destroyed"""
        self.health -= damage
        return self.health <= 0
    
    def get_rect(self):
        """Get collision rectangle"""
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class BossAlien:
    """Boss alien with multiple health and attacks"""
    def __init__(self, boss_type=0):
        # Get boss properties based on type
        boss_props = BOSS_TYPES[boss_type % len(BOSS_TYPES)]
        
        self.x = SCREEN_WIDTH // 2
        self.y = -100
        self.size = boss_props['size']
        self.speed = boss_props['speed']
        self.health = boss_props['health']
        self.max_health = boss_props['health']
        self.points = boss_props['points']
        self.shoot_rate = boss_props['shoot_rate']
        self.color = boss_props['color']
        self.boss_type = boss_props['name']
        self.boss_index = boss_type
        self.slime_pulse = 0
        
        self.direction = 1
        self.shoot_timer = 0
        self.phase = 0  # 0=entering, 1=attacking
        self.enter_timer = 0
        self.entered = False
        self.damage_flash = 0
        
        # Load image based on boss type
        self.image = None
        self.use_image = False
        
        # Try multiple boss images
        if boss_type % 3 == 0:  # Green boss
            image_path = BOSS_ENEMY_IMAGE_1
        else:  # Purple boss
            image_path = BOSS_ENEMY_IMAGE_2
            
        if os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
                self.use_image = True
                print(f"Loaded boss image: {image_path}")
            except Exception as e:
                print(f"Failed to load boss image: {e}")
        else:
            print(f"Boss image not found: {image_path}")
        
    def update(self):
        """Update boss movement and behavior"""
        self.slime_pulse += 0.03
        
        # Damage flash
        if self.damage_flash > 0:
            self.damage_flash -= 1
        
        if self.phase == 0:
            # Entering phase
            self.y += 2
            self.enter_timer += 1
            if self.y >= 100:
                self.phase = 1
                self.y = 100
                self.entered = True
        else:
            # Attack phase - side to side with slight vertical movement
            self.x += self.speed * self.direction
            
            # Bounce off walls
            if self.x > SCREEN_WIDTH - self.size - 10:
                self.direction = -1
            elif self.x < self.size + 10:
                self.direction = 1
            
            # Slight vertical oscillation
            self.y = 100 + math.sin(self.x / 100) * 20
            
            # Update shoot timer
            self.shoot_timer += 1
    
    def take_damage(self, damage=1):
        """Reduce health and return True if destroyed"""
        self.health -= damage
        self.damage_flash = 10
        if self.health <= 0:
            return True
        return False
    
    def should_shoot(self):
        """Check if boss should shoot"""
        if self.phase == 1 and self.shoot_timer >= self.shoot_rate:
            self.shoot_timer = 0
            return True
        return False
    
    def get_health_percentage(self):
        """Get boss health as percentage"""
        return max(0, (self.health / self.max_health) * 100)
    
    def get_rect(self):
        """Get collision rectangle"""
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Powerup:
    """Power-up that drops from aliens"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = POWERUP_SIZE
        self.speed = 1.5
        self.type = random.choice(['rapid_fire', 'spread_shot', 'shield'])
        self.angle = 0
        self.pulse = 0
        
        # Colors for different power-up types
        self.colors = {
            'rapid_fire': (255, 215, 0),  # Gold
            'spread_shot': (0, 255, 255),  # Cyan
            'shield': (0, 255, 0)  # Green
        }
        
        # Load image if available
        self.image = None
        self.use_image = False
        if os.path.exists(POWERUP_IMAGE):
            try:
                self.image = pygame.image.load(POWERUP_IMAGE)
                self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
                self.use_image = True
                print(f"Loaded powerup image: {POWERUP_IMAGE}")
            except Exception as e:
                print(f"Failed to load powerup image: {e}")
        else:
            print(f"Powerup image not found: {POWERUP_IMAGE}")
    
    def update(self):
        """Move power-up down with floating effect"""
        self.y += self.speed
        self.angle += 0.05
        self.pulse += 0.1
        return self.y > SCREEN_HEIGHT + 30
    
    def get_rect(self):
        """Get collision rectangle"""
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
    
    def get_color(self):
        """Get current color with pulsing effect"""
        base_color = self.colors.get(self.type, WHITE)
        pulse_factor = 0.7 + 0.3 * math.sin(self.pulse)
        return (int(base_color[0] * pulse_factor), 
                int(base_color[1] * pulse_factor), 
                int(base_color[2] * pulse_factor))

class EnemyBullet:
    """Bullet fired by enemies - shoots straight down"""
    def __init__(self, x, y):
        self.x = x
        self.y = y + 10
        self.size = ENEMY_BULLET_SIZE
        self.speed = ENEMY_BULLET_SPEED
        self.vy = self.speed  # Moves straight down
        
        # Trail effect
        self.trail = []
        self.max_trail = 8
    
    def update(self):
        """Move bullet straight down"""
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
        
        self.y += self.vy
        
        # Return True if off screen
        return self.y > SCREEN_HEIGHT + 50
    
    def get_rect(self):
        """Get collision rectangle"""
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class PlayerBullet:
    """Bullet fired by player - shoots straight up"""
    def __init__(self, x, y):
        self.x = x
        self.y = y - 20
        self.speed = PLAYER_BULLET_SPEED
        self.size = PLAYER_BULLET_SIZE
        self.vy = -self.speed  # Moves straight up
        self.damage = 1  # Default damage
        
        # Load image if available
        self.image = None
        self.use_image = False
        if os.path.exists(PLAYER_BULLET_IMAGE):
            try:
                self.image = pygame.image.load(PLAYER_BULLET_IMAGE)
                self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
                self.use_image = True
                print(f"Loaded player bullet image: {PLAYER_BULLET_IMAGE}")
            except Exception as e:
                print(f"Failed to load player bullet: {e}")
        else:
            print(f"Player bullet image not found: {PLAYER_BULLET_IMAGE}")
        
        # Trail effect
        self.trail = []
        self.max_trail = 5
    
    def update(self):
        """Move bullet straight up"""
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
        
        self.y += self.vy
        
        # Return True if off screen
        return self.y < -50
    
    def get_rect(self):
        """Get collision rectangle"""
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class BossBullet:
    """Bullet fired by boss - shoots at player (homing)"""
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y + 20
        self.size = BOSS_BULLET_SIZE
        
        # Load image if available
        self.image = None
        self.use_image = False
        if os.path.exists(BOSS_BULLET_IMAGE):
            try:
                self.image = pygame.image.load(BOSS_BULLET_IMAGE)
                self.image = pygame.transform.scale(self.image, (self.size * 2, self.size * 2))
                self.use_image = True
                print(f"Loaded boss bullet image: {BOSS_BULLET_IMAGE}")
            except Exception as e:
                print(f"Failed to load boss bullet: {e}")
        else:
            print(f"Boss bullet image not found: {BOSS_BULLET_IMAGE}")
        
        # Calculate direction to target (homing)
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist > 0:
            speed = BOSS_BULLET_SPEED
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0
            self.vy = speed
        
        # Trail effect
        self.trail = []
        self.max_trail = 10
    
    def update(self):
        """Move bullet toward target"""
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
        
        self.x += self.vx
        self.y += self.vy
        
        # Return True if off screen
        return (self.y > SCREEN_HEIGHT + 50 or self.y < -50 or 
                self.x > SCREEN_WIDTH + 50 or self.x < -50)
    
    def get_rect(self):
        """Get collision rectangle"""
        return (self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

class Star:
    """Background star with parallax effect"""
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.uniform(STAR_SIZE_MIN, STAR_SIZE_MAX)
        self.speed = random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX)
        self.brightness = random.uniform(0.3, 1.0)
        self.twinkle_offset = random.uniform(0, math.pi * 2)
        
    def update(self):
        """Update star position"""
        self.y -= self.speed
        if self.y < 0:
            self.y = SCREEN_HEIGHT
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def get_brightness(self, time):
        """Get current brightness with twinkling effect"""
        return self.brightness * (0.7 + 0.3 * math.sin(time + self.twinkle_offset))