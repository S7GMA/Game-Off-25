import pygame
import math
from settings import WIDTH, HEIGHT

class Transition:
    def __init__(self):
        self.active = False
        self.progress = 0
        self.color = (255, 255, 255)
        self.origin = (WIDTH // 2, HEIGHT // 2)

    def start(self, color, origin=None):
        """Begin the wave transition"""
        self.active = True
        self.progress = 0
        self.color = color
        if origin:
            self.origin = origin

    def update(self, dt):
        if not self.active:
            return False

        # Controls speed of wave spread
        self.progress += dt * 1.2

        if self.progress >= 1.0:
            self.active = False
            self.progress = 1.0
            return True  # Transition complete
        return False

    def draw(self, surface):
        if not self.active:
            return

        # ✅ Properly sized overlay surface
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        radius = int(max(WIDTH, HEIGHT) * self.progress * 1.5)
        alpha = int(255 * (1 - self.progress))

        # Expanding circle from the origin (usually player position)
        pygame.draw.circle(
            overlay,
            (*self.color, alpha),
            self.origin,
            radius
        )

        # Additive blending for glow effect
        surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
