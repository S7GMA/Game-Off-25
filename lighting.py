import pygame
import math
from settings import WIDTH, HEIGHT

class Lighting:
    """
    Dynamic gradient lighting system.
    Creates a smooth, shifting background that reacts subtly to player movement.
    """

    def __init__(self):
        self.t = 0  # internal time counter

    def draw_background(self, surface, tint=(0, 0, 0), player_pos=(0, 0)):
        self.t += 0.8
        px, py = player_pos

        # --- BASE GRADIENT ---
        gradient = pygame.Surface((WIDTH, HEIGHT))
        base_color = pygame.Color(*tint)

        # Slightly brighter and darker variations of the tint
        darker = base_color.correct_gamma(0.5)
        lighter = base_color.correct_gamma(1.5)

        # Generate vertical gradient with motion wave
        for y in range(HEIGHT):
            # Movement tied to player + time = organic "liquid" motion
            wave = math.sin((y * 0.015) + (self.t * 0.05) + (px + py) * 0.002)
            mix = max(0, min(1, (y / HEIGHT) + wave * 0.15))
            r = int(darker.r * (1 - mix) + lighter.r * mix)
            g = int(darker.g * (1 - mix) + lighter.g * mix)
            b = int(darker.b * (1 - mix) + lighter.b * mix)
            pygame.draw.line(gradient, (r, g, b), (0, y), (WIDTH, y))

        # --- LIQUID SHIMMER EFFECT ---
        shimmer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for i in range(6):
            offset = int(math.sin(self.t * 0.03 + i) * 120)
            color = (*tint, 40)
            pygame.draw.circle(
                shimmer,
                color,
                (WIDTH // 2 + offset, HEIGHT // 2 + offset // 2),
                500,
            )

        # Blend the shimmer over the gradient for a smooth “underwater” look
        gradient.blit(shimmer, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # --- DARKENING & TINT OVERLAY ---
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 90))  # base darkness
        tint_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        tint_surface.fill((*tint, 35))  # subtle tint
        overlay.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Combine and draw to main screen
        gradient.blit(overlay, (0, 0))
        surface.blit(gradient, (0, 0))
