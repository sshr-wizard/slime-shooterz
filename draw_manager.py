"""
Slime Shooterz - Drawing Functions
Developed by MANBOY
"""

import pygame
import math
from constants import *

class DrawManager:
    """Manages all drawing operations"""
    
    @staticmethod
    def draw_player(screen, player):
        x, y = player.x, player.y
        
        if player.invincible and player.invincible_timer % 10 < 5:
            return
        
        if player.powerup_active:
            glow_color = {
                'rapid_fire': (255, 215, 0),
                'spread_shot': (0, 255, 255),
                'shield': (0, 255, 0)
            }.get(player.powerup_type, (255, 255, 255))
            
            pulse = 0.7 + 0.3 * math.sin(pygame.time.get_ticks() / 200)
            glow_size = int(player.size * 1.5 * pulse)
            glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*glow_color, 50), (glow_size, glow_size), glow_size)
            screen.blit(glow_surf, (x - glow_size, y - glow_size))
        
        if player.use_image and player.image:
            rect = player.image.get_rect(center=(x, y))
            screen.blit(player.image, rect)
            return
        
        # Slime-style player ship
        pygame.draw.ellipse(screen, (0, 200, 100), 
                           (x - player.size, y - player.size * 0.8, 
                            player.size * 2, player.size * 1.6))
        pygame.draw.ellipse(screen, (0, 255, 150), 
                           (x - player.size * 0.8, y - player.size * 0.6, 
                            player.size * 1.6, player.size * 1.2))
        pygame.draw.circle(screen, CYAN, (x, y - player.size * 0.2), player.size * 0.3)
        pygame.draw.circle(screen, (100, 255, 255), (x, y - player.size * 0.2), player.size * 0.2)
        
        for i in range(3):
            alpha = 150 - i * 30
            size = 5 - i
            pygame.draw.circle(screen, (0, 255, 100), 
                             (x - 5 + i * 5, y + player.size * 0.6 + i * 3), size)
    
    @staticmethod
    def draw_alien(screen, alien):
        x, y = alien.x, alien.y
        size = alien.size
        pulse = 1 + 0.1 * math.sin(alien.slime_pulse)
        
        if alien.use_image and alien.image:
            rect = alien.image.get_rect(center=(x, y))
            screen.blit(alien.image, rect)
            return
        
        color = (136, 255, 0)
        
        pygame.draw.ellipse(screen, color, 
                           (x - size * pulse, y - size * 0.7 * pulse, 
                            size * 2 * pulse, size * 1.4 * pulse))
        pygame.draw.ellipse(screen, (200, 255, 100), 
                           (x - size * 0.6 * pulse, y - size * 0.4 * pulse, 
                            size * 1.2 * pulse, size * 0.8 * pulse))
        
        eye_offset = size * 0.3
        eye_size = size * 0.25
        pygame.draw.circle(screen, WHITE, (int(x - eye_offset), int(y - eye_offset * 0.3)), int(eye_size))
        pygame.draw.circle(screen, WHITE, (int(x + eye_offset), int(y - eye_offset * 0.3)), int(eye_size))
        pygame.draw.circle(screen, BLACK, (int(x - eye_offset + 2), int(y - eye_offset * 0.3)), int(eye_size * 0.5))
        pygame.draw.circle(screen, BLACK, (int(x + eye_offset + 2), int(y - eye_offset * 0.3)), int(eye_size * 0.5))
    
    @staticmethod
    def draw_boss(screen, boss):
        if boss is None:
            return
        
        x, y = boss.x, boss.y
        size = boss.size
        pulse = 1 + 0.1 * math.sin(boss.slime_pulse)
        
        if boss.damage_flash > 0 and boss.damage_flash % 4 < 2:
            return
        
        if boss.use_image and boss.image:
            rect = boss.image.get_rect(center=(x, y))
            screen.blit(boss.image, rect)
            return
        
        color = boss.color if hasattr(boss, 'color') else LIME
        
        pygame.draw.ellipse(screen, color, 
                           (x - size * pulse, y - size * 0.9 * pulse, 
                            size * 2 * pulse, size * 1.8 * pulse))
        
        inner_color = (color[0] + 50, color[1] + 50, color[2] + 50) if color != PURPLE else (200, 50, 200)
        pygame.draw.ellipse(screen, inner_color, 
                           (x - size * 0.7 * pulse, y - size * 0.5 * pulse, 
                            size * 1.4 * pulse, size * 1.0 * pulse))
        
        for i in range(3):
            crown_x = x - size * 0.4 + i * size * 0.4
            crown_y = y - size * 0.8 * pulse
            pygame.draw.circle(screen, GOLD, (int(crown_x), int(crown_y)), int(size * 0.15))
        
        eye_offset = size * 0.35
        eye_size = size * 0.3
        pygame.draw.circle(screen, RED, (int(x - eye_offset), int(y - eye_offset * 0.3)), int(eye_size))
        pygame.draw.circle(screen, RED, (int(x + eye_offset), int(y - eye_offset * 0.3)), int(eye_size))
        pygame.draw.circle(screen, YELLOW, (int(x - eye_offset + 2), int(y - eye_offset * 0.3)), int(eye_size * 0.5))
        pygame.draw.circle(screen, YELLOW, (int(x + eye_offset + 2), int(y - eye_offset * 0.3)), int(eye_size * 0.5))
    
    @staticmethod
    def draw_powerup(screen, powerup):
        x, y = powerup.x, powerup.y
        size = powerup.size
        color = powerup.get_color()
        
        glow_size = int(size * 1.5)
        glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, 80), (glow_size, glow_size), glow_size)
        screen.blit(glow_surf, (x - glow_size, y - glow_size))
        
        if powerup.use_image and powerup.image:
            rect = powerup.image.get_rect(center=(x, y))
            screen.blit(powerup.image, rect)
        else:
            points = []
            for i in range(10):
                angle = i * math.pi / 5 + powerup.angle
                radius = size if i % 2 == 0 else size * 0.5
                px = x + radius * math.cos(angle)
                py = y + radius * math.sin(angle)
                points.append((px, py))
            pygame.draw.polygon(screen, color, points)
            pygame.draw.polygon(screen, WHITE, points, 2)
        
        font = pygame.font.Font(None, 14)
        label = font.render(powerup.type.replace('_', ' ').title(), True, WHITE)
        screen.blit(label, (x - label.get_width() // 2, y + size + 5))
    
    @staticmethod
    def draw_player_bullet(screen, bullet):
        x, y = bullet.x, bullet.y
        size = bullet.size
        
        for i, pos in enumerate(bullet.trail):
            alpha = int(255 * (i / len(bullet.trail)))
            trail_size = size * (i / len(bullet.trail))
            pygame.draw.circle(screen, (100, 255, 100, alpha), 
                             (int(pos[0]), int(pos[1])), int(trail_size))
        
        if bullet.use_image and bullet.image:
            rect = bullet.image.get_rect(center=(x, y))
            screen.blit(bullet.image, rect)
            return
        
        pygame.draw.circle(screen, (200, 255, 150), (int(x), int(y)), size * 2)
        pygame.draw.circle(screen, LIME, (int(x), int(y)), size)
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), size * 0.5)
    
    @staticmethod
    def draw_boss_bullet(screen, bullet):
        x, y = bullet.x, bullet.y
        size = bullet.size
        
        for i, pos in enumerate(bullet.trail):
            alpha = int(255 * (i / len(bullet.trail)))
            trail_size = size * (i / len(bullet.trail))
            pygame.draw.circle(screen, (255, 100, 100, alpha), 
                             (int(pos[0]), int(pos[1])), int(trail_size))
        
        if bullet.use_image and bullet.image:
            rect = bullet.image.get_rect(center=(x, y))
            screen.blit(bullet.image, rect)
            return
        
        pygame.draw.circle(screen, (255, 150, 150), (int(x), int(y)), size * 2)
        pygame.draw.circle(screen, RED, (int(x), int(y)), size)
        pygame.draw.circle(screen, ORANGE, (int(x), int(y)), size * 0.5)
    
    @staticmethod
    def draw_enemy_bullet(screen, bullet):
        x, y = bullet.x, bullet.y
        size = bullet.size
        
        for i, pos in enumerate(bullet.trail):
            alpha = int(200 * (i / len(bullet.trail)))
            trail_size = size * (i / len(bullet.trail)) * 0.8
            pygame.draw.circle(screen, (200, 255, 100, alpha), 
                             (int(pos[0]), int(pos[1])), int(trail_size))
        
        pygame.draw.circle(screen, (200, 255, 100), (int(x), int(y)), size * 1.5)
        pygame.draw.circle(screen, LIME, (int(x), int(y)), size)
        pygame.draw.circle(screen, WHITE, (int(x), int(y)), size * 0.5)
    
    @staticmethod
    def draw_stars(screen, stars, time):
        for star in stars:
            brightness = int(255 * star.get_brightness(time))
            pygame.draw.circle(screen, (brightness, brightness, brightness),
                             (int(star.x), int(star.y)), int(star.size))