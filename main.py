import pygame
import sys
import random
import math
import os 
from player import Player
from wave import Wave
from lighting import Lighting
from enemy import Enemy
from settings import *
from pickup import Pickup
from transition import Transition
from death_effect import DeathEffect
from level import Level
from sound import SoundManager

pygame.init()

#DEBUG: mixer + paths
print("MIXER INIT:", pygame.mixer.get_init())
print("WORKING DIR:", os.getcwd())
print("PLUCK EXISTS:", os.path.exists("assets/sounds/pluck.wav"))

# --- Setup Window ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Echo Game - Game Off 2025")
clock = pygame.time.Clock()

# --- Helper: Screen Shake ---
def apply_screen_shake(intensity):
    offset_x = random.randint(-intensity, intensity)
    offset_y = random.randint(-intensity, intensity)
    return offset_x, offset_y

# -----------------------------------------------------
# MENU DRAW FUNCTION
# -----------------------------------------------------
def draw_menu():
    screen.fill((10, 10, 15))

    title_font = pygame.font.Font(None, 120)
    menu_font = pygame.font.Font(None, 60)

    title = title_font.render("E C H O   W A V E", True, (0, 200, 255))
    start = menu_font.render("Click to Start", True, (255, 255, 255))
    quit_text = menu_font.render("Press Q to Quit", True, (200, 200, 200))

    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 80))

    pygame.display.flip()

# -----------------------------------------------------
#NEW: COUNTDOWN FUNCTION (SAFE + ISOLATED)
# -----------------------------------------------------
def run_countdown():
    countdown_font = pygame.font.Font(None, 180)
    numbers = ["3", "2", "1", "GO!"]

    for n in numbers:
        screen.fill((0, 0, 0))

        text = countdown_font.render(n, True, (0, 200, 255))
        screen.blit(text, (WIDTH//2 - text.get_width()//2,
                           HEIGHT//2 - text.get_height()//2))

        pygame.display.flip()
        pygame.time.delay(700)  # 0.7 seconds each

# --- Main Game Loop ---
def main():
    player = Player(WIDTH // 2, HEIGHT // 2)
    waves = []
    enemies = []
    pickups = []
    lighting = Lighting()
    transition = Transition()
    effects = []  # 💥 for hybrid death effects
    level = Level()  # ✅ new level manager instance

    # initialize sound
    sound = SoundManager()
    sound.load_sound("shoot", "assets/sounds/pluck_boosted.wav", volume=1.0)
    print("LOADED SOUNDS (after init):", sound.sounds)  # 🔍 DEBUG

    bg_color = level.get_color()

    level_timer = 0
    spawn_timer = 0
    level_done = False
    score = 0
    lives = 3
    health = 100

    shake_timer = 0
    shake_intensity = 0
    invincible_timer = 0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                waves.append(Wave(player.rect.center, pygame.mouse.get_pos(), level.get_color()))
                sound.play("shoot")  # 🔊 play shooting wave SFX

            # reset player speed when boost timer ends
            if event.type == pygame.USEREVENT + 1:
                player.speed = PLAYER_SPEED

        # --- Update ---
        player.update(dt)
        for wave in waves:
            wave.update(dt)
        waves = [w for w in waves if not w.finished]

        # Update hybrid death effects
        for e in effects[:]:
            e.update(dt)
            if not e.alive:
                effects.remove(e)

        # Wave collision inversion
        for i in range(len(waves)):
            for j in range(i + 1, len(waves)):
                waves[i].collide_with(waves[j])

        # --- Enemy Spawning ---
        level_timer += dt
        if not level_done:
            spawn_timer += dt
            if spawn_timer >= level.spawn_rate:
                spawn_timer = 0
                side = random.choice(["top", "bottom", "left", "right"])
                if side == "top":
                    x, y = random.randint(0, WIDTH), -20
                elif side == "bottom":
                    x, y = random.randint(0, WIDTH), HEIGHT + 20
                elif side == "left":
                    x, y = -20, random.randint(0, HEIGHT)
                else:
                    x, y = WIDTH + 20, random.randint(0, HEIGHT)

                enemy_color = level.get_color()
                enemies.append(Enemy(x, y, (255, 255, 255)))
                print(f"Spawned enemy at ({x}, {y}) - Color: {enemy_color}")

        # --- Enemy Update ---
        for enemy in enemies:
            enemy.update(dt, player.rect.center)

        # --- Player Collision / Damage ---
        player_center = pygame.Vector2(player.rect.center)
        for enemy in enemies:
            if (enemy.pos - player_center).length() < enemy.radius + 5:
                if not hasattr(player, "invincible") or not player.invincible:
                    health -= 20
                    shake_timer = 0.2
                    shake_intensity = 5
                    player.invincible = True
                    invincible_timer = 1.0

                    if health <= 0:
                        lives -= 1
                        health = 100
                        if lives <= 0:
                            print("GAME OVER")
                            running = False

        # --- Invincibility Timer ---
        if hasattr(player, "invincible") and player.invincible:
            invincible_timer -= dt
            if invincible_timer <= 0:
                player.invincible = False

        # --- Wave Hits Enemy ---
        for wave in waves[:]:
            for enemy in enemies[:]:
                dist = math.hypot(wave.x - enemy.pos.x, wave.y - enemy.pos.y)
                if dist < wave.radius + enemy.radius:
                    if enemy.take_damage(1):
                        enemies.remove(enemy)
                        score += 100
                        shake_timer = 0.3
                        shake_intensity = 6

                        # Spawn hybrid death effect
                        effects.append(DeathEffect(enemy.pos.x, enemy.pos.y, level.get_color()))

                        # 10% chance to drop a pickup
                        if random.random() < 0.1:
                            pickups.append(Pickup(enemy.pos.x, enemy.pos.y, "speed"))

                        if not getattr(wave, "piercing", False):
                            wave.finished = True
                            break
                    else:
                        if not getattr(wave, "piercing", False):
                            wave.finished = True
                            break

        # --- Pickup Update ---
        for pickup in pickups[:]:
            pickup.update(dt)
            if pickup.collected:
                pickups.remove(pickup)
                continue

            player_center = pygame.Vector2(player.rect.center)
            if (player_center - pickup.pos).length() < 30:
                pickup.collected = True
                pickups.remove(pickup)
                player.speed *= 1.3
                pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

        # --- Level Progression ---
        if not level_done and level_timer >= level.duration:
            level_done = True
            print("Clear Remaining Enemies")

        if level_done and len(enemies) == 0 and not transition.active:
            transition.start(level.get_color(), player.rect.center)

        if transition.active:
            done = transition.update(dt)
            if done:
                level_done = False
                level_timer = 0
                level.next_level()
                bg_color = level.get_color()
                print(f"WAVE COMPLETE -> Level {level.index}")

        # --- Screen Shake ---
        shake_offset = (0, 0)
        if shake_timer > 0:
            shake_timer -= dt
            shake_offset = apply_screen_shake(shake_intensity)

        # --- Draw ---
        screen.fill(bg_color)
        lighting.draw_background(screen, tint=level.get_color(), player_pos=player.rect.center)

        for wave in waves:
            wave.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for pickup in pickups:
            pickup.draw(screen)
        for e in effects:
            e.draw(screen)

        # --- Player Blink When Invincible ---
        if hasattr(player, "invincible") and player.invincible:
            if int(pygame.time.get_ticks() / 100) % 2 == 0:
                pass
            else:
                player.draw(screen)
        else:
            player.draw(screen)

        # --- Apply Screen Shake ---
        if shake_offset != (0, 0):
            shaken = pygame.Surface((WIDTH, HEIGHT))
            shaken.blit(screen, shake_offset)
            screen.blit(shaken, (0, 0))

        # --- HUD ---
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        health_text = font.render(f"Health: {health}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level.index + 1}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        screen.blit(health_text, (20, 55))
        screen.blit(lives_text, (20, 90))
        screen.blit(level_text, (WIDTH - 160, 20))

        if level_done:
            remaining_text = font.render(f"Enemies Remaining: {len(enemies)}", True, (255, 255, 0))
            screen.blit(remaining_text, (WIDTH - 600, 20))

        transition.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
