"""
Slime Shooterz - UI Rendering
Developed by MANBOY
"""

import pygame
import math
from constants import *

class UIManager:
    """Manages all UI rendering"""
    
    def __init__(self):
        self.font = None
        self.small_font = None
        self.large_font = None
        self.dev_font = None
        self._init_fonts()
    
    def _init_fonts(self):
        try:
            self.font = pygame.font.Font(None, UI_FONT_SIZE)
            self.small_font = pygame.font.Font(None, 24)
            self.large_font = pygame.font.Font(None, GAME_OVER_FONT_SIZE)
            self.dev_font = pygame.font.Font(None, 16)
        except:
            self.font = pygame.font.SysFont('Arial', UI_FONT_SIZE)
            self.small_font = pygame.font.SysFont('Arial', 24)
            self.large_font = pygame.font.SysFont('Arial', GAME_OVER_FONT_SIZE)
            self.dev_font = pygame.font.SysFont('Arial', 16)
    
    def draw_hud(self, screen, state):
        score = state['score']
        lives = state['lives']
        boss_defeated = state.get('boss_defeated', 0)
        kills = state.get('kills', 0)
        
        # Score
        score_text = self.font.render(f"Score: {score}", True, LIME)
        screen.blit(score_text, (UI_PADDING, UI_PADDING))
        
        # Kills counter
        kills_text = self.small_font.render(f"Kills: {kills}", True, WHITE)
        screen.blit(kills_text, (UI_PADDING, UI_PADDING + 40))
        
        # Boss defeated count
        if boss_defeated > 0:
            boss_text = self.small_font.render(f"Bosses: {boss_defeated}", True, PURPLE)
            screen.blit(boss_text, (UI_PADDING, UI_PADDING + 65))
        
        # Lives with hearts
        hearts = "♥" * lives
        lives_text = self.font.render(f"Lives: {hearts}", True, RED)
        screen.blit(lives_text, (SCREEN_WIDTH - 200, UI_PADDING))
        
        # Enemy count
        enemy_text = self.small_font.render(f"Enemies: {state.get('enemy_count', 0)}", True, (128, 128, 128))
        screen.blit(enemy_text, (SCREEN_WIDTH - 200, UI_PADDING + 45))
        
        # Power-up indicator
        if state.get('powerup_active', False):
            self._draw_powerup_indicator(screen, state)
        
        # Next boss indicator
        if not state['boss_active'] and not state['game_over']:
            next_boss = state['next_boss_score']
            color = LIME if next_boss - score <= 20 else (128, 128, 128)
            next_boss_text = self.small_font.render(f"Next Boss: {next_boss}", True, color)
            y_pos = UI_PADDING + 90 if boss_defeated > 0 else UI_PADDING + 65
            screen.blit(next_boss_text, (UI_PADDING, y_pos))
        
        # Boss warning
        if state['boss_warning']:
            self._draw_boss_warning(screen, state['boss_warning_timer'])
        
        # Boss health bar
        if state['boss_active']:
            self._draw_boss_health_bar(screen, state['boss_health'], state.get('boss_name', 'BOSS'))
        
        # Developer credit
        dev_text = self.dev_font.render(DEVELOPER, True, (64, 64, 64))
        screen.blit(dev_text, (SCREEN_WIDTH - dev_text.get_width() - 10, SCREEN_HEIGHT - 25))
    
    def _draw_powerup_indicator(self, screen, state):
        powerup_type = state.get('powerup_type', '')
        timer = state.get('powerup_timer', 0)
        duration = state.get('powerup_duration', POWERUP_DURATION)
        
        colors = {
            'rapid_fire': (255, 215, 0),
            'spread_shot': (0, 255, 255),
            'shield': (0, 255, 0)
        }
        color = colors.get(powerup_type, WHITE)
        
        bar_width = 200
        bar_height = 15
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = UI_PADDING
        
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        progress = timer / duration
        pygame.draw.rect(screen, color, (bar_x, bar_y, int(bar_width * (1 - progress)), bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        labels = {
            'rapid_fire': '[RAPID FIRE]',
            'spread_shot': '[SPREAD SHOT]',
            'shield': '[SHIELD]'
        }
        label_text = labels.get(powerup_type, powerup_type.upper())
        label = self.small_font.render(label_text, True, color)
        screen.blit(label, (bar_x + bar_width // 2 - label.get_width() // 2, bar_y - 22))
    
    def _draw_boss_warning(self, screen, timer):
        pulse = 0.5 + 0.5 * abs(math.sin(pygame.time.get_ticks() / 200))
        
        overlay = pygame.Surface((SCREEN_WIDTH, 100))
        overlay.set_alpha(int(50 * pulse))
        overlay.fill((255, 0, 0))
        screen.blit(overlay, (0, SCREEN_HEIGHT // 2 - 50))
        
        warning_font = pygame.font.Font(None, 48)
        color = (255, int(255 * pulse), int(255 * pulse))
        warning_text = warning_font.render("NYAMBALIZO IKUBWELA!", True, color)
        screen.blit(warning_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 40))
        
        countdown_text = self.font.render(f"Get ready! {BOSS_WARNING_DURATION - timer}", True, WHITE)
        screen.blit(countdown_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 20))
    
    def _draw_boss_health_bar(self, screen, health_percentage, boss_name="BOSS"):
        bar_x = SCREEN_WIDTH // 2 - BOSS_HEALTH_BAR_WIDTH // 2
        bar_y = BOSS_HEALTH_BAR_Y
        
        pygame.draw.rect(screen, DARK_RED, 
                        (bar_x, bar_y, BOSS_HEALTH_BAR_WIDTH, BOSS_HEALTH_BAR_HEIGHT))
        
        if health_percentage > 60:
            color = LIME
        elif health_percentage > 30:
            color = YELLOW
        else:
            color = RED
        
        pygame.draw.rect(screen, color,
                        (bar_x, bar_y, 
                         int(BOSS_HEALTH_BAR_WIDTH * (health_percentage / 100)),
                         BOSS_HEALTH_BAR_HEIGHT))
        
        pygame.draw.rect(screen, WHITE,
                        (bar_x, bar_y, BOSS_HEALTH_BAR_WIDTH, BOSS_HEALTH_BAR_HEIGHT), 2)
        
        boss_label = self.small_font.render(f"[{boss_name}]", True, color)
        screen.blit(boss_label, (bar_x - 80, bar_y + 2))
        
        hp_text = self.small_font.render(f"{int(health_percentage)}%", True, WHITE)
        screen.blit(hp_text, (bar_x + BOSS_HEALTH_BAR_WIDTH + 10, bar_y + 2))
    
    def draw_game_over(self, screen, score):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Movie-style game over
        title_font = pygame.font.Font(None, 80)
        game_over_text = title_font.render("SLIME SHOOTERZ", True, LIME)
        
        # Glow effect
        for offset in range(4, 0, -1):
            glow_surf = title_font.render("SLIME SHOOTERZ", True, (0, 50 + offset * 10, 0))
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2 - offset, 
                                   SCREEN_HEIGHT // 2 - 120 - offset))
        
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))
        
        # "THE END" style
        the_end_font = pygame.font.Font(None, 60)
        the_end_text = the_end_font.render("WAZEPULIDWA", True, RED)
        screen.blit(the_end_text, (SCREEN_WIDTH // 2 - the_end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        score_text = self.font.render(f"Final Score: {score}", True, YELLOW)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        pulse = 0.7 + 0.3 * abs(math.sin(pygame.time.get_ticks() / 500))
        color = (int(255 * pulse), int(255 * pulse), int(255 * pulse))
        restart_text = self.font.render("Press R to Restart", True, color)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        
        dev_text = self.small_font.render(f"~ {DEVELOPER} ~", True, (64, 255, 64))
        screen.blit(dev_text, (SCREEN_WIDTH // 2 - dev_text.get_width() // 2, SCREEN_HEIGHT // 2 + 110))
    
    def draw_welcome(self, screen):
        """Welcome screen - movie poster style"""
        # Title with glow
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("SLIME SHOOTERZ", True, LIME)
        
        # Glow effect
        for offset in range(6, 0, -1):
            glow_surf = title_font.render("SLIME SHOOTERZ", True, (0, 50 + offset * 10, 0))
            screen.blit(glow_surf, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 - offset, 
                                   SCREEN_HEIGHT // 2 - 160 - offset))
        
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 160))
        
        # Subtitle
        sub_font = pygame.font.Font(None, 28)
        sub_text = sub_font.render("Aliens are friends, we just don't understand them yet...", True, (136, 255, 0))
        screen.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2, SCREEN_HEIGHT // 2 - 110))
        
        # Decorative line
        for i in range(SCREEN_WIDTH // 2 - 100, SCREEN_WIDTH // 2 + 100):
            if i % 3 == 0:
                pygame.draw.line(screen, (50, 150, 50), (i, SCREEN_HEIGHT // 2 - 85), (i + 2, SCREEN_HEIGHT // 2 - 80), 2)
        
        # Start button - movie style
        pulse = 0.7 + 0.3 * abs(math.sin(pygame.time.get_ticks() / 500))
        color = (int(255 * pulse), int(255 * pulse), int(100 * pulse))
        start_text = self.font.render("▶ PRESS SPACE TO START", True, color)
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        
        # Controls - movie credits style
        controls = [
            "DIRECTIZO: MANBOY",
            "STARRING: The Slime Aliens",
            "",
            "CONTROLS",
            "  Mouse Click / SPACE  -  Shoot",
            "  Arrow Keys          -  Move"
        ]
        y_offset = 20
        for i, text in enumerate(controls):
            if "DIRECTIZO" in text or "STARRING" in text:
                font = self.small_font
                color = (180, 180, 180)
            elif "CONTROLS" in text:
                font = self.small_font
                color = (255, 215, 0)
            elif text.startswith("  "):
                font = self.small_font
                color = (150, 150, 150)
            else:
                continue
            
            control_text = font.render(text, True, color)
            screen.blit(control_text, (SCREEN_WIDTH // 2 - control_text.get_width() // 2, 
                                      SCREEN_HEIGHT // 2 + y_offset + i * 25))
        
        # Developer credit
        dev_text = self.dev_font.render(f"~ {DEVELOPER} ~", True, (64, 255, 64))
        screen.blit(dev_text, (SCREEN_WIDTH // 2 - dev_text.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def draw_controls_hint(self, screen):
        hint_text = self.small_font.render("Click/SPACE: Shoot | Arrow Keys: Move | R: Restart", 
                                          True, (128, 128, 128))
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2, SCREEN_HEIGHT - 20))