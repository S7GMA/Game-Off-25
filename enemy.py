import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, color=(255, 50, 50)):
        self.pos = pygame.Vector2(x, y)
        self.color = color
        self.radius = 15
        self.speed = 100
        self.health = 1

    def update(self, dt, player_pos):
        # Move toward player
        direction = pygame.Vector2(player_pos) - self.pos
        distance = direction.length()
        if distance != 0:
            direction = direction.normalize()
        self.pos += direction * self.speed * dt

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0  # True if enemy dies

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
