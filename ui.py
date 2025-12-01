import pygame
from settings import WIDTH, HEIGHT

class UI:
    def __init__(self):
        self.font_main = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)

    def draw_hud(self, surface, score, health, lives, level):
        """Draws the in-game heads-up display (HUD)."""
        score_text = self.font_main.render(f"Score: {score}", True, (255, 255, 255))
        health_text = self.font_main.render(f"Health: {health}", True, (255, 255, 255))
        lives_text = self.font_main.render(f"Lives: {lives}", True, (255, 255, 255))
        level_text = self.font_main.render(f"Level: {level + 1}", True, (255, 255, 255))

        surface.blit(score_text, (20, 20))
        surface.blit(health_text, (20, 55))
        surface.blit(lives_text, (20, 90))
        surface.blit(level_text, (WIDTH - 160, 20))

    def draw_center_text(self, surface, text, color=(255, 255, 255)):
        """Draw large centered messages like 'PAUSED' or 'LEVEL COMPLETE'."""
        label = self.font_large.render(text, True, color)
        rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        surface.blit(label, rect)
