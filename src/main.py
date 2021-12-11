import pygame
import random

from src.ships.Enemy import Enemy
from src.constants import WIDTH, HEIGHT, WIN, BACKGROUND, FPS, FONT_FAMILY
from src.ships.Player import Player
from src.utils import collide

pygame.font.init()


def main():
    run = 1
    level = 1
    lives = 5
    font_size = 25
    main_font = pygame.font.SysFont(FONT_FAMILY, font_size)
    lost_font = pygame.font.SysFont(FONT_FAMILY, font_size)

    lost = False
    lost_count = 0

    enemies = []

    wave_level = 5

    enemy_vel = 1

    player_vel = 5

    laser_vel = 5

    player = Player(WIDTH / 2, HEIGHT - 115)

    clock = pygame.time.Clock()

    def redraw_window():
        # BG
        WIN.blit(BACKGROUND, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        levels_label = main_font.render(f"Level: {level}", True, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render('Busted.!!!', True, (255, 255, 255))
            WIN.blit(lost_label,
                     (int(WIDTH / 2 - lost_label.get_width() / 2), int(HEIGHT / 2 - lost_label.get_height() / 2)))

        pygame.display.update()

    while run:

        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_level += 5
            for i in range(wave_level):
                xx = random.randrange(50, WIDTH - 100)
                yy = random.randrange(-1500, -100)
                color = random.choice(["red", "green", "blue"])
                # health = 100 if color == "green" else 200 if color == "blue" else 300
                enemy = Enemy(xx, yy, color)
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and (player.x - player_vel > 0):  # left
            player.x -= player_vel

        if keys[pygame.K_d] and (player.x + player_vel + player.get_width() < WIDTH):  # right
            player.x += player_vel

        if keys[pygame.K_w] and (player.y - player_vel > 0):  # up
            player.y -= player_vel

        if keys[pygame.K_s] and (player.y + player_vel + player.get_height() + 15 < HEIGHT):  # down
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)


def main_menu():
    font_size = 50
    title_font = pygame.font.SysFont(FONT_FAMILY, font_size)
    run = True
    while run:
        WIN.blit(BACKGROUND, (0, 0))
        title_label = title_font.render("Press mouse button to begin...", True, (255, 255, 255))
        WIN.blit(title_label,
                 (int(WIDTH / 2 - title_label.get_width() / 2), int(HEIGHT / 2 - title_label.get_height() / 2)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()
