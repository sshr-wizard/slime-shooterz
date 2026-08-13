"""
Slime Shooterz - Main Game
Developed by MANBOY
"""

import pygame
import sys
import math
import os
from constants import *
from game_manager import GameManager
from ui_manager import UIManager
from draw_manager import DrawManager

class SlimeShooterz:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        
        # Set window icon BEFORE creating the window
        try:
            # Try multiple locations for the icon
            icon_paths = [
                get_resource_path("icon.ico"),
                "icon.ico",
                get_resource_path("logo.png"),
                "logo.png",
                get_resource_path("assets/logo.png"),
                "assets/logo.png"
            ]
            
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    icon = pygame.image.load(icon_path)
                    # Scale icon to 32x32 for window title bar
                    icon = pygame.transform.scale(icon, (32, 32))
                    pygame.display.set_icon(icon)
                    print(f"Window icon set from: {icon_path}")
                    break
        except Exception as e:
            print(f"Failed to set window icon: {e}")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        
        pygame.mouse.set_visible(False)
        
        self.game_manager = GameManager()
        self.ui_manager = UIManager()
        self.draw_manager = DrawManager()
        
        self.game_state = "LOADING"  # LOADING, MENU, PLAYING, GAME_OVER
        self.running = True
        self.loading_progress = 0
        self.loading_text_index = 0
        self.loading_timer = 0
        
        # Load logo for background
        self.logo = None
        self.logo_loaded = False
        self.logo_original = None
        self._load_logo()
        
        self.story_lines = [
            "",
            "THE SLIME INVASION",
            "",
            "They came from the void...",
            "Green. Slimy. Hungry.",
            "",
            "Our satellite array was destroyed.",
            "Their slime ships blotted out the sun.",
            "They wanted Earth...",
            "",
            "But one pilot stood against the tide.",
            "A spaceman. A warrior.",
            "",
            "MANBOY",
            "",
            "Now he fights alone.",
            "In the slime-infested void.",
            "For humanity's last hope.",
            "",
            "",
            "★ PRESS SPACE TO BEGIN ★"
        ]
        
        self.game_manager.setup()
    
    def _load_logo(self):
        """Load logo for background - handles all sizes"""
        # Check multiple possible locations
        logo_paths = [
            get_resource_path("logo.png"),
            get_resource_path("assets/logo.png"),
            "logo.png",
            "assets/logo.png"
        ]
        
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                try:
                    # Load original logo without scaling first
                    self.logo_original = pygame.image.load(logo_path)
                    
                    # Get original dimensions
                    orig_width = self.logo_original.get_width()
                    orig_height = self.logo_original.get_height()
                    
                    print(f"Logo loaded: {orig_width}x{orig_height} from {logo_path}")
                    
                    # Calculate scale to fit screen (70% of screen size, maintain aspect ratio)
                    scale_x = SCREEN_WIDTH / orig_width
                    scale_y = SCREEN_HEIGHT / orig_height
                    scale = min(scale_x, scale_y) * 0.7  # 70% of screen size
                    
                    # Ensure minimum size
                    min_scale = 0.3
                    if scale < min_scale:
                        scale = min_scale
                    
                    new_width = int(orig_width * scale)
                    new_height = int(orig_height * scale)
                    
                    # Ensure minimum dimensions
                    if new_width < 100:
                        new_width = 100
                    if new_height < 100:
                        new_height = 100
                    
                    # Scale the logo
                    self.logo = pygame.transform.scale(self.logo_original, (new_width, new_height))
                    self.logo_loaded = True
                    print(f"Logo scaled to: {new_width}x{new_height}")
                    return
                except Exception as e:
                    print(f"Failed to load logo from {logo_path}: {e}")
        
        print("Logo not found. Using slime background only.")
        self.logo_loaded = False
    
    def run(self):
        """Main game loop"""
        while self.running:
            self._handle_events()
            
            if self.game_state == "LOADING":
                self._update_loading()
            
            elif self.game_state == "MENU":
                pass
            
            elif self.game_state == "PLAYING":
                keys = pygame.key.get_pressed()
                self.game_manager.update(keys)
                
                if self.game_manager.game_over:
                    self.game_state = "GAME_OVER"
            
            self._draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def _update_loading(self):
        """Update loading screen animation"""
        self.loading_timer += 1
        
        # Slower text reveal for dramatic effect
        if self.loading_timer >= 120:  # 2 seconds per line
            self.loading_timer = 0
            self.loading_text_index += 1
            self.loading_progress = min(100, self.loading_progress + 5)
            
            if self.loading_text_index >= len(self.story_lines):
                self.game_state = "MENU"
    
    def _handle_events(self):
        """Handle all events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_state == "LOADING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_state = "MENU"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.game_state = "MENU"
                continue
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.game_state == "PLAYING":
                        self.game_manager.set_mouse_pressed(True)
                    elif self.game_state == "MENU":
                        self.game_state = "PLAYING"
                        self.game_manager.setup()
                        self.game_manager.stop_music()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.game_state == "PLAYING":
                        self.game_manager.set_mouse_pressed(False)
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == "MENU":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "PLAYING"
                        self.game_manager.setup()
                        self.game_manager.stop_music()
                
                elif self.game_state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        self.game_state = "PLAYING"
                        self.game_manager.setup()
                        self.game_manager.game_over = False
                        self.game_manager.stop_music()
                
                elif self.game_state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        self.game_manager.shoot_bullet()
    
    def _draw(self):
        """Draw everything"""
        self.screen.fill((0, 10, 0))
        
        if self.game_state == "LOADING":
            self._draw_loading()
        elif self.game_state == "MENU":
            self.draw_manager.draw_stars(self.screen, self.game_manager.stars, self.game_manager.time)
            self.ui_manager.draw_welcome(self.screen)
            self.ui_manager.draw_controls_hint(self.screen)
        elif self.game_state == "PLAYING":
            self.draw_manager.draw_stars(self.screen, self.game_manager.stars, self.game_manager.time)
            self._draw_game()
        elif self.game_state == "GAME_OVER":
            self.draw_manager.draw_stars(self.screen, self.game_manager.stars, self.game_manager.time)
            self._draw_game()
            self.ui_manager.draw_game_over(self.screen, self.game_manager.score)
        
        pygame.display.flip()
    
    def _draw_loading(self):
        """Draw loading screen with movie-style presentation and logo background"""
        # Dark atmosphere
        self.screen.fill((5, 0, 5))
        
        # Draw logo as faint background
        if self.logo_loaded and self.logo:
            try:
                # Create a transparent version of the logo
                logo_copy = self.logo.copy()
                logo_copy.set_alpha(30)  # Very faint (30 out of 255)
                
                # Center the logo
                logo_x = SCREEN_WIDTH // 2 - logo_copy.get_width() // 2
                logo_y = SCREEN_HEIGHT // 2 - logo_copy.get_height() // 2
                self.screen.blit(logo_copy, (logo_x, logo_y))
                
                # Add a second layer with even less opacity for glow effect
                logo_glow = self.logo.copy()
                logo_glow.set_alpha(15)
                glow_offset = 10
                self.screen.blit(logo_glow, (logo_x - glow_offset, logo_y - glow_offset))
            except Exception as e:
                print(f"Error displaying logo: {e}")
        
        # Draw slime blobs in background (creepy atmosphere)
        for i in range(8):
            x = (i * 120 + self.loading_timer * 0.15) % SCREEN_WIDTH
            y = (i * 80 + self.loading_timer * 0.2) % SCREEN_HEIGHT
            size = 40 + math.sin(self.loading_timer * 0.015 + i) * 20
            color = (0, 60 + int(30 * math.sin(self.loading_timer * 0.02 + i)), 0)
            pygame.draw.ellipse(self.screen, color,
                               (int(x - size/2), int(y - size/2), int(size), int(size * 1.3)))
        
        # Title - Movie style
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("SLIME SHOOTERZ", True, (136, 255, 0))
        title_glow = title_font.render("SLIME SHOOTERZ", True, (0, 100, 0))
        
        # Glow effect for title
        for offset in range(5, 0, -1):
            glow_surf = title_font.render("SLIME SHOOTERZ", True, (0, 50 + offset * 10, 0))
            self.screen.blit(glow_surf, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 - offset, 20 - offset))
        
        self.screen.blit(title_glow, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 3, 23))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))
        
        # Fancy divider
        for i in range(SCREEN_WIDTH):
            if i % 4 == 0:
                height = 80 + 20 * math.sin(i / 50 + self.loading_timer * 0.02)
                pygame.draw.line(self.screen, (50, 150, 50), (i, height - 10), (i, height + 10), 2)
                pygame.draw.line(self.screen, (20, 80, 20), (i, height - 5), (i, height + 5), 1)
        
        # Story text - Large, movie-style
        y_offset = 150
        
        # Show current text with movie-style presentation
        for i in range(max(0, self.loading_text_index - 2), self.loading_text_index + 1):
            if i < len(self.story_lines):
                text = self.story_lines[i]
                if text == "":
                    y_offset += 30
                    continue
                
                # Different text sizes for different elements
                if text == "MANBOY":
                    font = pygame.font.Font(None, 80)
                    color = (255, 215, 0)
                    shadow_color = (80, 60, 0)
                    y_offset += 10
                elif text == "★ PRESS SPACE TO BEGIN ★":
                    font = pygame.font.Font(None, 40)
                    color = (255, 255, 100)
                    pulse = 0.7 + 0.3 * math.sin(self.loading_timer * 0.05)
                    color = (int(255 * pulse), int(255 * pulse), int(100 * pulse))
                    shadow_color = (40, 40, 0)
                elif text == "THE SLIME INVASION":
                    font = pygame.font.Font(None, 56)
                    color = (200, 50, 50)
                    shadow_color = (60, 10, 10)
                elif text.startswith("★"):
                    font = pygame.font.Font(None, 36)
                    color = (200, 200, 200)
                    shadow_color = (40, 40, 40)
                elif "SLIME" in text.upper() or "VOID" in text.upper():
                    font = pygame.font.Font(None, 40)
                    color = (136, 255, 0)
                    shadow_color = (0, 60, 0)
                elif "EARTH" in text.upper() or "HUMANITY" in text.upper():
                    font = pygame.font.Font(None, 40)
                    color = (100, 200, 255)
                    shadow_color = (0, 40, 80)
                elif "DESTROYED" in text.upper() or "ATTACK" in text.upper() or "BLOTTED" in text.upper():
                    font = pygame.font.Font(None, 40)
                    color = (200, 50, 50)
                    shadow_color = (60, 10, 10)
                elif "FIGHT" in text.upper() or "WARRIOR" in text.upper():
                    font = pygame.font.Font(None, 44)
                    color = (255, 150, 50)
                    shadow_color = (60, 30, 0)
                else:
                    font = pygame.font.Font(None, 38)
                    color = (200, 200, 200)
                    shadow_color = (40, 40, 40)
                
                # Movie-style text reveal with fade-in
                if i == self.loading_text_index:
                    # Current text - fully visible with glow
                    text_surf = font.render(text, True, color)
                    
                    # Shadow effect
                    if 'shadow_color' in locals():
                        shadow_surf = font.render(text, True, shadow_color)
                        x_pos = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
                        self.screen.blit(shadow_surf, (x_pos + 3, y_offset + 3))
                    
                    # Glow effect for important text
                    if text == "MANBOY" or text == "THE SLIME INVASION":
                        for j in range(3, 0, -1):
                            glow_surf = font.render(text, True, (color[0]//4, color[1]//4, color[2]//4))
                            self.screen.blit(glow_surf, (x_pos - j, y_offset - j))
                    
                    self.screen.blit(text_surf, (x_pos, y_offset))
                else:
                    # Previous text - dimmed but visible (like movie credits)
                    dim_color = (80, 80, 80)
                    text_surf = font.render(text, True, dim_color)
                    x_pos = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
                    self.screen.blit(text_surf, (x_pos, y_offset))
                
                y_offset += 55
        
        # Progress bar (bottom)
        bar_width = 400
        bar_height = 8
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = SCREEN_HEIGHT - 60
        
        pygame.draw.rect(self.screen, (20, 20, 20), (bar_x, bar_y, bar_width, bar_height))
        
        progress = min(100, self.loading_text_index * 100 / len(self.story_lines))
        if progress > 0:
            pygame.draw.rect(self.screen, (50, 200, 50), 
                           (bar_x, bar_y, int(bar_width * progress / 100), bar_height))
            # Glow effect
            glow_size = 15
            glow_surf = pygame.Surface((bar_width * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (50, 255, 50, 30), 
                           (0, 0, int(bar_width * progress / 100), glow_size * 2))
            self.screen.blit(glow_surf, (bar_x - glow_size, bar_y - glow_size))
        
        pygame.draw.rect(self.screen, (50, 150, 50), (bar_x, bar_y, bar_width, bar_height), 1)
        
        progress_text = pygame.font.Font(None, 20).render(f"{int(progress)}%", True, (100, 200, 100))
        self.screen.blit(progress_text, (SCREEN_WIDTH // 2 - progress_text.get_width() // 2, bar_y - 22))
        
        dots = "." * (int(self.loading_timer / 20) % 4)
        loading_text = pygame.font.Font(None, 20).render(f"Loading{dots}", True, (100, 200, 100))
        self.screen.blit(loading_text, (SCREEN_WIDTH // 2 - loading_text.get_width() // 2, bar_y + 15))
        
        skip_text = pygame.font.Font(None, 16).render("Press SPACE or Click to Skip", True, (60, 60, 60))
        self.screen.blit(skip_text, (SCREEN_WIDTH // 2 - skip_text.get_width() // 2, SCREEN_HEIGHT - 20))
    
    def _draw_game(self):
        """Draw game objects"""
        # Draw power-ups
        for powerup in self.game_manager.powerups:
            self.draw_manager.draw_powerup(self.screen, powerup)
        
        # Draw player
        self.draw_manager.draw_player(self.screen, self.game_manager.player)
        
        # Draw aliens
        for alien in self.game_manager.aliens:
            self.draw_manager.draw_alien(self.screen, alien)
        
        # Draw boss
        if self.game_manager.boss_active and self.game_manager.boss:
            self.draw_manager.draw_boss(self.screen, self.game_manager.boss)
        
        # Draw bullets
        for bullet in self.game_manager.player_bullets:
            self.draw_manager.draw_player_bullet(self.screen, bullet)
        
        for bullet in self.game_manager.boss_bullets:
            self.draw_manager.draw_boss_bullet(self.screen, bullet)
        
        for bullet in self.game_manager.enemy_bullets:
            self.draw_manager.draw_enemy_bullet(self.screen, bullet)
        
        # Draw HUD
        state = self.game_manager.get_state()
        self.ui_manager.draw_hud(self.screen, state)
        self.ui_manager.draw_controls_hint(self.screen)

def main():
    game = SlimeShooterz()
    game.run()

if __name__ == "__main__":
    main()