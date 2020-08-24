import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")
TO_ASSETS = "assets"
# ENIMY SHIP 
SPACE_SHIP_RED = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
SPACE_SHIP_GREEN = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
SPACE_SHIP_BLUE = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# PLAYER SHIP
SPACE_SHIP_YELLOW = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

#LASERS
LASER_RED = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
LASER_GREEN = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
LASER_BLUE = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
LASER_YELLOW = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

# BACKGROUND IMAGE
bg_image =  pygame.image.load(os.path.join("assets", "background-black.png"))
BACKGROUND = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.ship_img = SPACE_SHIP_YELLOW
        self.laser_img = LASER_YELLOW
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        'red': (SPACE_SHIP_RED, LASER_RED),
        'blue': (SPACE_SHIP_BLUE, LASER_BLUE),
        'green': (SPACE_SHIP_GREEN, LASER_GREEN)
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel


def main():
    run = 1
    FPS = 60
    level = 1
    lives = 5
    font_family = "comicsans"
    font_size = 25
    main_font = pygame.font.SysFont(font_family, font_size)

    enemies = []

    wave_level = 5
    enemy_vel = 1

    player_val = 5

    player = Player((WIDTH/3)-25, (HEIGHT/3)-25)

    clock = pygame.time.Clock()
    def redraw_window():
        #BG
        WIN.blit(BACKGROUND, (0, 0))
        
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        levels_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))
        
        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()
    while run:

        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_level += 5
            for i in range(wave_level):
                xx = random.randrange(50, WIDTH - 100)
                yy = random.randrange(-1500, -100)
                color = random.choice(["red", "green", "blue"])
                #health = 100 if color == "green" else 200 if color == "blue" else 300
                enemy = Enemy(xx, yy, color)
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        key = pygame.key.get_pressed()

        if key[pygame.K_a] and (player.x - player_val > 0): #left
            player.x -= player_val
        
        if key[pygame.K_d] and (player.x + player_val + player.get_width() < WIDTH): #right
            player.x += player_val

        if key[pygame.K_w] and (player.y - player_val > 0): #up
            player.y -= player_val
        
        if key[pygame.K_s] and (player.y + player_val + player.get_height() < HEIGHT): #down
            player.y += player_val

        for enemy in enemies[:]:
            enemy.move(player_val)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()


                


if __name__ == '__main__':
    main()