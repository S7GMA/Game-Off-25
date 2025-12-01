import pygame
import random

class Pickup:
    def __init__(self, x, y, type="speed"):
        self.pos = pygame.Vector2(x, y)
        self.type = type
        self.size = 15
        self.color =  (255,255, 0) # bright yellow for speed boost
        self.collected = False
        self.timer = 15 # seconds before it disappear

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.collected = True

    def draw(self, surface):
        points = [
            (self.pos.x, self.pos.y - self.size),
            (self.pos.x - self.size, self.pos.y + self.size),
            (self.pos.x + self.size, self.pos.y + self.size),

        ]
        pygame.draw.polygon(surface, self.color, points)