import pygame
import math
import random
from settings import WIDTH, HEIGHT

class Wave:
    def __init__(self, start_pos, target_pos, color=(0, 180, 255)):
        self.x, self.y = start_pos
        tx, ty = target_pos
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 0.1
        self.dx, self.dy = dx / dist, dy / dist
        self.speed = 400
        self.radius = 2  # smaller initial wave
        self.max_radius = 300  # tighter expansion = limits basically
        self.finished = False
        self.base_color = color
        self.alpha = 180
        self.invert_timer = 0
        self.particles = []  # spark storage
        self.piercing = False

        # Bounce and waveform properties
        self.bounces_left = 2
        self.wave_amplitude = 6
        self.wave_frequency = 12

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        self.radius += 120 * dt

        if self.invert_timer > 0:
            self.invert_timer -= 1

        # Bounce off screen edges
        bounced = False
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.dx *= -1
            bounced = True
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.dy *= -1
            bounced = True

        if bounced:
            self.bounces_left -= 1
            self.radius *= 0.75
            self.alpha *= 0.85

            # create visible spark burst when bouncing
            for _ in range(10):
                angle = math.radians(random.randint(0, 360))
                speed = random.uniform(60, 140)
                self.particles.append({
                    "x": self.x,
                    "y": self.y,
                    "dx": math.cos(angle) * speed,
                    "dy": math.sin(angle) * speed,
                    "life": random.uniform(0.4, 0.8),
                    "color": tuple(min(255, c + 100) for c in self.base_color),  # brighter sparks
                })

        # Update and fade particles
        for p in self.particles[:]:
            p["x"] += p["dx"] * dt
            p["y"] += p["dy"] * dt
            p["life"] -= dt
            if p["life"] <= 0:
                self.particles.remove(p)

        # smooth fade out (end of players wave life)
        # smooth fade-out for all waves (works on every bounce)
        life_ratio = min(1.0, self.radius / self.max_radius)
        self.alpha = max(0, 180 * (1 - life_ratio ** 1.5))

        if self.radius > self.max_radius or self.bounces_left <= 0:
            self.finished = True

    def collide_with(self, other):
        """If two waves overlap visually, trigger an invert flash."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        if distance < (self.radius + other.radius) * 0.5:
            self.invert_timer = 10
            other.invert_timer = 10

    def draw(self, surface):
        # Dynamic hue cycling
        hue_shift = (pygame.time.get_ticks() * 0.1) % 360
        color_obj = pygame.Color(0)
        color_obj.hsva = (hue_shift, 100, 100, 100)
        draw_color = (color_obj.r, color_obj.g, color_obj.b)

        if self.invert_timer > 0:
            draw_color = (255 - draw_color[0], 255 - draw_color[1], 255 - draw_color[2])

        alpha = max(0, self.alpha - (self.radius / self.max_radius) * self.alpha * 2)
        wave_surf = pygame.Surface((self.radius * 2 + 10, self.radius * 2 + 10), pygame.SRCALPHA)

        # WiFi arc settings
        t = pygame.time.get_ticks() * 0.005
        spread = 150  # total degrees wide of the arc
        layers = 3  # number of arcs (like WiFi bands)
        spacing = 15  # distance between each arc
        angle_center = math.degrees(math.atan2(self.dy, self.dx))
        start_angle = angle_center - spread / 2
        end_angle = angle_center + spread / 2

        # Draw several arcs that radiate outward
        for i in range(layers):
            layer_radius = self.radius - (i * spacing)
            if layer_radius <= 0:
                continue

            points = []
            for angle in range(int(start_angle), int(end_angle), 4):
                rad = math.radians(angle)
                wobble = math.sin(rad * self.wave_frequency + t + i) * (self.wave_amplitude * 0.7)
                r = layer_radius + wobble
                x = int(r * math.cos(rad) + self.radius)
                y = int(r * math.sin(rad) + self.radius)
                points.append((x, y))

            if len(points) > 2:
                pygame.draw.lines(wave_surf, (*draw_color, int(alpha * (1 - i * 0.3))), False, points, width=4 - i)

        # Combine the arcs with additive blending for glow
        surface.blit(
            wave_surf,
            (self.x - self.radius, self.y - self.radius),
            special_flags=pygame.BLEND_ADD,
        )

        # Draw small fading sparks (safe color conversion)
        for p in self.particles:
            spark_alpha = max(0, min(255, int(255 * (p["life"] / 0.8))))
            color = tuple(int(min(255, max(0, c))) for c in p["color"])
            pos = (int(p["x"]), int(p["y"]))

            # core spark
            pygame.draw.circle(surface, (*color, spark_alpha), pos, 3)
            # halo glow
            pygame.draw.circle(surface, (*color, spark_alpha // 3), pos, 6, 1)
