import pygame
from settings import *
import math
from collections import deque

class Player:
    def __init__(self, x, y):
        # Player base image
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 200), (20, 20), 18)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_SPEED
        self.angle = 0

        # --- Trail System ---
        self.trail = deque(maxlen=10)  # store last 10 positions
        self.trail_alpha_decay = 25    # transparency fade per segment

    def update(self, dt):
        # Mouse position and movement
        mx, my = pygame.mouse.get_pos()
        px, py = self.rect.center

        dx, dy = mx - px, my - py
        dist = math.hypot(dx, dy)

        # Store position for trail when moving
        if dist > 1:
            self.trail.appendleft(self.rect.center)

        # Movement
        if dist > 5:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed * dt
            self.rect.y += dy * self.speed * dt

        # Rotate player to face mouse
        self.angle = math.degrees(math.atan2(-dy, dx))

    def draw(self, surface):
        # --- Draw Trail (fades behind player) ---
        for i, pos in enumerate(self.trail):
            alpha = max(0, 255 - i * self.trail_alpha_decay)
            trail_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(trail_surf, (0, 255, 200, alpha), (20, 20), 18)
            surface.blit(trail_surf, (pos[0] - 20, pos[1] - 20))

        # --- Draw Main Player ---
        surface.blit(self.image, self.rect)
