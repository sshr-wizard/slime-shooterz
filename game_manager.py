"""
Slime Shooterz - Game Logic
Developed by MANBOY
"""

import pygame
import random
import math
import os
from constants import *
from entities import *

class GameManager:
    """Manages all game logic and state"""
    
    def __init__(self):
        self.player = None
        self.aliens = []
        self.boss = None
        self.player_bullets = []
        self.boss_bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.stars = []
        self.score = 0
        self.game_over = False
        self.boss_active = False
        self.boss_warning = False
        self.boss_warning_timer = 0
        self.boss_spawn_score = BOSS_SPAWN_SCORE
        self.enemy_timer = 0
        self.boss_defeated_count = 0
        self.boss_type = 0
        self.time = 0
        self.kills = 0
        
        # Mouse state
        self.mouse_pressed = False
        self.shoot_cooldown = 0
        
        # Sound objects
        self.sounds = {}
        self.sound_enabled = False
        self.gun_channels = []
        self.next_channel = 0
        self.music_channel = None
        self.music_playing = False
        
        # Initialize stars
        self.stars = [Star() for _ in range(STAR_COUNT)]
        
    def setup(self):
        """Initialize or reset the game"""
        self.player = Player()
        self.aliens = []
        self.boss = None
        self.player_bullets = []
        self.boss_bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.score = 0
        self.game_over = False
        self.boss_active = False
        self.boss_warning = False
        self.boss_warning_timer = 0
        self.boss_spawn_score = BOSS_SPAWN_SCORE
        self.enemy_timer = 0
        self.boss_defeated_count = 0
        self.boss_type = 0
        self.shoot_cooldown = 0
        self.gun_channels = []
        self.next_channel = 0
        self.kills = 0
        
        # Load sounds (but don't restart music if already playing)
        self._load_sounds()
    
    def _load_sounds(self):
        """Load sound effects"""
        try:
            pygame.mixer.init()
            pygame.mixer.set_num_channels(32)
            self.sound_enabled = True
            
            sound_files = {
                'gun': GUN_SOUND,
                'enemy_death': ENEMY_DEATH_SOUND,
                'boss_explosion': BOSS_EXPLOSION_SOUND,
                'boss_shot': BOSS_SHOT_SOUND,
                'player_hit': PLAYER_HIT_SOUND,
                'game_over': GAME_OVER_SOUND,
                'enemy_shoot': ENEMY_SHOOT_SOUND,
                'powerup': POWERUP_SOUND,
                'boss_warning': BOSS_WARNING_SOUND,
                'background_music': BACKGROUND_MUSIC
            }
            
            for name, path in sound_files.items():
                if os.path.exists(path):
                    try:
                        self.sounds[name] = pygame.mixer.Sound(path)
                        print(f"Loaded sound: {path}")
                    except Exception as e:
                        print(f"Failed to load {path}: {e}")
                else:
                    print(f"Sound file not found: {path}")
                    
            self.gun_channels = []
            for i in range(8):
                channel = pygame.mixer.Channel(i)
                self.gun_channels.append(channel)
            self.next_channel = 0
                    
            if not self.sounds:
                self.sound_enabled = False
                
        except Exception as e:
            print(f"Sound initialization failed: {e}")
            self.sound_enabled = False
        
        # Start background music if not already playing
        if not self.music_playing:
            self._start_music()
    
    def _start_music(self):
        """Start background music on a dedicated channel"""
        if not self.sound_enabled:
            return
        
        try:
            # Get a dedicated channel for music
            self.music_channel = pygame.mixer.Channel(15)  # Use last channel for music
            if 'background_music' in self.sounds and self.sounds['background_music']:
                self.music_channel.play(self.sounds['background_music'], loops=-1)  # Loop forever
                self.music_playing = True
                print("Background music started")
            else:
                print("Background music file not found or not loaded")
        except Exception as e:
            print(f"Failed to start background music: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if self.music_channel and self.music_playing:
            try:
                self.music_channel.stop()
                self.music_playing = False
                print("Background music stopped")
            except Exception as e:
                print(f"Failed to stop music: {e}")
    
    def play_sound(self, sound_name):
        """Play a sound"""
        if not self.sound_enabled or sound_name not in self.sounds:
            return
        
        try:
            if sound_name == 'gun':
                channel = self.gun_channels[self.next_channel]
                self.next_channel = (self.next_channel + 1) % len(self.gun_channels)
                if channel.get_busy():
                    channel.stop()
                channel.play(self.sounds['gun'])
            else:
                channel = pygame.mixer.find_channel()
                if channel:
                    channel.play(self.sounds[sound_name])
                else:
                    self.sounds[sound_name].play()
        except Exception as e:
            pass
    
    def set_mouse_pressed(self, pressed):
        self.mouse_pressed = pressed
    
    def update(self, keys):
        """Update all game logic"""
        self.time += 0.01
        
        if self.game_over:
            return
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        self.player.update(keys)
        
        if self.mouse_pressed and self.shoot_cooldown == 0:
            self.shoot_bullet()
            self.shoot_cooldown = 4
        
        # Update stars
        for star in self.stars:
            star.update()
        
        # Spawn aliens
        self._spawn_aliens()
        
        # Check boss spawn
        self._check_boss_spawn()
        
        # Update aliens and handle shooting
        for alien in self.aliens[:]:
            if alien.update():
                self.aliens.remove(alien)
            else:
                if alien.should_shoot():
                    self._alien_shoot(alien)
        
        # Update boss
        if self.boss_active and self.boss is not None:
            self.boss.update()
            if self.boss.should_shoot():
                self._boss_shoot()
        
        # Update bullets
        for bullet in self.player_bullets[:]:
            if bullet.update():
                self.player_bullets.remove(bullet)
        
        for bullet in self.boss_bullets[:]:
            if bullet.update():
                self.boss_bullets.remove(bullet)
        
        for bullet in self.enemy_bullets[:]:
            if bullet.update():
                self.enemy_bullets.remove(bullet)
        
        # Update powerups
        for powerup in self.powerups[:]:
            if powerup.update():
                self.powerups.remove(powerup)
        
        # Handle collisions
        self._handle_collisions()
        
        # Update score
        self.score = self.player.score
    
    def _spawn_aliens(self):
        """Spawn aliens"""
        if self.boss_active:
            return
        
        self.enemy_timer += 1
        if (self.enemy_timer >= EASY_ENEMY_SPAWN_RATE and 
            len(self.aliens) < MAX_EASY_ENEMIES):
            self.aliens.append(SlimeAlien())
            self.enemy_timer = 0
    
    def _check_boss_spawn(self):
        """Check if boss should spawn"""
        if (not self.boss_active and 
            self.score >= self.boss_spawn_score and 
            not self.game_over):
            
            if not self.boss_warning:
                self.boss_warning = True
                self.boss_warning_timer = 0
                self.play_sound('boss_warning')
                print("BOSS WARNING!")
            
            self.boss_warning_timer += 1
            if self.boss_warning_timer >= BOSS_WARNING_DURATION:
                self._spawn_boss()
    
    def _spawn_boss(self):
        if not self.boss_active:
            self.boss = BossAlien(self.boss_type)
            self.boss_active = True
            self.boss_warning = False
            boss_name = BOSS_TYPES[self.boss_type % len(BOSS_TYPES)]['name']
            print(f"{boss_name} SPAWNED! Score: {self.score}")
    
    def _boss_shoot(self):
        if self.boss and len(self.boss_bullets) < MAX_BOSS_BULLETS:
            bullet = BossBullet(
                self.boss.x,
                self.boss.y,
                self.player.x,
                self.player.y
            )
            self.boss_bullets.append(bullet)
            self.play_sound('boss_shot')
    
    def _alien_shoot(self, alien):
        if len(self.enemy_bullets) < MAX_ENEMY_BULLETS:
            bullet = EnemyBullet(alien.x, alien.y)
            self.enemy_bullets.append(bullet)
            self.play_sound('enemy_shoot')
    
    def _drop_powerup(self, x, y):
        if random.random() < POWERUP_DROP_CHANCE:
            powerup = Powerup(x, y)
            self.powerups.append(powerup)
    
    def shoot_bullet(self):
        if self.game_over:
            return
        
        if self.player.powerup_active and self.player.powerup_type == 'spread_shot':
            spread_offsets = [-15, 0, 15]
            for offset in spread_offsets:
                if len(self.player_bullets) < MAX_POWERUP_BULLETS:
                    bullet = PlayerBullet(self.player.x + offset, self.player.y)
                    self.player_bullets.append(bullet)
            self.play_sound('gun')
            
        elif self.player.powerup_active and self.player.powerup_type == 'rapid_fire':
            for _ in range(2):
                if len(self.player_bullets) < MAX_POWERUP_BULLETS:
                    bullet = PlayerBullet(self.player.x, self.player.y)
                    bullet.speed = PLAYER_BULLET_SPEED * 1.5
                    bullet.vy = -bullet.speed
                    self.player_bullets.append(bullet)
            self.play_sound('gun')
        
        elif self.player.powerup_active and self.player.powerup_type == 'shield':
            if len(self.player_bullets) < MAX_POWERUP_BULLETS:
                bullet = PlayerBullet(self.player.x, self.player.y)
                bullet.size = PLAYER_BULLET_SIZE * 2
                bullet.damage = 2
                self.player_bullets.append(bullet)
                self.play_sound('gun')
        
        else:
            if len(self.player_bullets) < MAX_PLAYER_BULLETS:
                bullet = PlayerBullet(self.player.x, self.player.y)
                self.player_bullets.append(bullet)
                self.play_sound('gun')
    
    def _handle_collisions(self):
        """Handle all collisions"""
        
        # Player Bullet vs Aliens
        for bullet in self.player_bullets[:]:
            bullet_rect = bullet.get_rect()
            for alien in self.aliens[:]:
                alien_rect = alien.get_rect()
                if self._rect_collision(bullet_rect, alien_rect):
                    damage = getattr(bullet, 'damage', 1)
                    if alien.take_damage(damage):
                        alien_x, alien_y = alien.x, alien.y
                        self.aliens.remove(alien)
                        self.player.score += alien.points
                        self.kills += 1
                        self.play_sound('enemy_death')
                        self._drop_powerup(alien_x, alien_y)
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    break
        
        # Player Bullet vs Boss
        if self.boss_active and self.boss is not None:
            for bullet in self.player_bullets[:]:
                bullet_rect = bullet.get_rect()
                boss_rect = self.boss.get_rect()
                if self._rect_collision(bullet_rect, boss_rect):
                    damage = getattr(bullet, 'damage', 1)
                    boss_x, boss_y = self.boss.x, self.boss.y
                    boss_points = self.boss.points
                    boss_type_index = self.boss_type
                    
                    if self.boss.take_damage(damage):
                        self.boss_active = False
                        self.player.score += boss_points
                        self.boss_defeated_count += 1
                        self.kills += 1
                        self.boss_spawn_score += 100 * (self.boss_defeated_count + 1)
                        self.boss_type += 1
                        self.boss = None
                        self.play_sound('boss_explosion')
                        self._drop_powerup(boss_x, boss_y)
                        boss_name = BOSS_TYPES[boss_type_index % len(BOSS_TYPES)]['name']
                        print(f"{boss_name} DEFEATED! Score: {self.score}")
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    break
        
        # Check if player has shield
        has_shield = self.player.powerup_active and self.player.powerup_type == 'shield'
        
        # Enemy Bullet vs Player (no shield)
        if not has_shield and not self.player.invincible and not self.game_over:
            player_rect = self.player.get_rect()
            for bullet in self.enemy_bullets[:]:
                bullet_rect = bullet.get_rect()
                if self._rect_collision(player_rect, bullet_rect):
                    self.enemy_bullets.remove(bullet)
                    if self.player.hit():
                        self.play_sound('player_hit')
                    if self.player.lives <= 0:
                        self.game_over = True
                        self.play_sound('game_over')
                        self.stop_music()
        
        # Boss Bullet vs Player (no shield)
        if not has_shield and not self.player.invincible and not self.game_over:
            player_rect = self.player.get_rect()
            for bullet in self.boss_bullets[:]:
                bullet_rect = bullet.get_rect()
                if self._rect_collision(player_rect, bullet_rect):
                    self.boss_bullets.remove(bullet)
                    if self.player.hit():
                        self.play_sound('player_hit')
                    if self.player.lives <= 0:
                        self.game_over = True
                        self.play_sound('game_over')
                        self.stop_music()
        
        # Player vs Aliens (no shield)
        if not has_shield and not self.player.invincible and not self.game_over:
            player_rect = self.player.get_rect()
            for alien in self.aliens[:]:
                alien_rect = alien.get_rect()
                if self._rect_collision(player_rect, alien_rect):
                    self.aliens.remove(alien)
                    if self.player.hit():
                        self.play_sound('player_hit')
                    if self.player.lives <= 0:
                        self.game_over = True
                        self.play_sound('game_over')
                        self.stop_music()
        
        # Player vs Boss (no shield)
        if not has_shield and self.boss_active and self.boss is not None and not self.player.invincible and not self.game_over:
            player_rect = self.player.get_rect()
            boss_rect = self.boss.get_rect()
            if self._rect_collision(player_rect, boss_rect):
                boss_x, boss_y = self.boss.x, self.boss.y
                boss_points = self.boss.points
                boss_type_index = self.boss_type
                
                self.boss.take_damage(2)
                if self.boss.health <= 0:
                    self.boss_active = False
                    self.player.score += boss_points
                    self.boss_defeated_count += 1
                    self.kills += 1
                    self.boss_spawn_score += 100 * (self.boss_defeated_count + 1)
                    self.boss_type += 1
                    self.boss = None
                    self.play_sound('boss_explosion')
                    self._drop_powerup(boss_x, boss_y)
                    boss_name = BOSS_TYPES[boss_type_index % len(BOSS_TYPES)]['name']
                    print(f"{boss_name} DEFEATED! Score: {self.score}")
                if self.player.hit():
                    self.play_sound('player_hit')
                if self.player.lives <= 0:
                    self.game_over = True
                    self.play_sound('game_over')
                    self.stop_music()
        
        # Player vs Powerup
        if not self.game_over:
            player_rect = self.player.get_rect()
            for powerup in self.powerups[:]:
                powerup_rect = powerup.get_rect()
                if self._rect_collision(player_rect, powerup_rect):
                    self.powerups.remove(powerup)
                    self.player.activate_powerup(powerup.type)
                    self.play_sound('powerup')
        
        # Shield: destroy bullets
        if has_shield and not self.game_over:
            player_rect = self.player.get_rect()
            for bullet in self.enemy_bullets[:]:
                bullet_rect = bullet.get_rect()
                if self._rect_collision(player_rect, bullet_rect):
                    self.enemy_bullets.remove(bullet)
            
            for bullet in self.boss_bullets[:]:
                bullet_rect = bullet.get_rect()
                if self._rect_collision(player_rect, bullet_rect):
                    self.boss_bullets.remove(bullet)
    
    @staticmethod
    def _rect_collision(rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
    
    def get_state(self):
        boss_health = 0
        boss_name = ""
        if self.boss_active and self.boss is not None:
            boss_health = self.boss.get_health_percentage()
            boss_name = self.boss.boss_type if hasattr(self.boss, 'boss_type') else "BOSS"
        
        return {
            'score': self.score,
            'lives': self.player.lives,
            'game_over': self.game_over,
            'boss_active': self.boss_active,
            'boss_health': boss_health,
            'boss_name': boss_name,
            'boss_warning': self.boss_warning,
            'boss_warning_timer': self.boss_warning_timer,
            'next_boss_score': self.boss_spawn_score,
            'boss_defeated': self.boss_defeated_count,
            'enemy_count': len(self.aliens),
            'kills': self.kills,
            'bullet_count': len(self.player_bullets),
            'powerup_active': self.player.powerup_active,
            'powerup_type': self.player.powerup_type,
            'powerup_timer': self.player.powerup_timer,
            'powerup_duration': POWERUP_DURATION
        }