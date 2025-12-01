import pygame
import random
import math

class DeathEffect:
    def __init__(self, x, y, color):
        # Ensure color is always RGB tuple and bright enough
        self.color = tuple(max(60, int(c)) for c in color[:3])

        self.x = x
        self.y = y
        self.particles = []
        self.radius = 0
        self.alpha = 255
        self.alive = True

        # Create initial spark burst
        for _ in range(16):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(140, 280)
            self.particles.append({
                "x": x,
                "y": y,
                "dx": math.cos(angle) * speed,
                "dy": math.sin(angle) * speed,
                "life": random.uniform(0.6, 1.0)
            })

    def update(self, dt):
        """Expand shockwave and fade particles"""
        self.radius += 260 * dt
        self.alpha -= 200 * dt
        if self.alpha <= 0 and len(self.particles) == 0:
            self.alive = False

        # Update sparks
        for p in self.particles[:]:
            p["x"] += p["dx"] * dt
            p["y"] += p["dy"] * dt
            p["life"] -= dt * 1.1
            if p["life"] <= 0:
                self.particles.remove(p)

    def draw(self, surface):
        """Draw both shockwave ring and fading sparks"""
        safe_color = tuple(max(0, min(255, int(c))) for c in self.color)

        # --- Draw expanding shockwave ring ---
        if self.alpha > 0:
            ring_alpha = max(0, int(self.alpha))
            glow_alpha = int(self.alpha // 3)

            ring_color = (*safe_color, ring_alpha)
            glow_color = (*safe_color, glow_alpha)

            # Outer glow for soft fade
            pygame.draw.circle(surface, glow_color, (int(self.x), int(self.y)), int(self.radius) + 6, 8)
            # Main crisp ring
            pygame.draw.circle(surface, ring_color, (int(self.x), int(self.y)), int(self.radius), 3)

        # --- Draw glowing spark particles ---
        for p in self.particles:
            alpha = max(0, min(255, int(255 * (p["life"] / 0.8))))
            pygame.draw.circle(surface, (*safe_color, alpha), (int(p["x"]), int(p["y"])), 3)
            # Add slight halo for smoother feel
            pygame.draw.circle(surface, (*safe_color, alpha // 3), (int(p["x"]), int(p["y"])), 6, 1)
