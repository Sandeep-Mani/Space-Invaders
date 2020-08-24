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
SPACE_SHIP_RED = pygame.image.load(
    os.path.join("assets", "pixel_ship_red_small.png"))
SPACE_SHIP_GREEN = pygame.image.load(
    os.path.join("assets", "pixel_ship_green_small.png"))
SPACE_SHIP_BLUE = pygame.image.load(
    os.path.join("assets", "pixel_ship_blue_small.png"))

# PLAYER SHIP
SPACE_SHIP_YELLOW = pygame.image.load(
    os.path.join("assets", "pixel_ship_yellow.png"))

# LASERS
LASER_RED = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
LASER_GREEN = pygame.image.load(
    os.path.join("assets", "pixel_laser_green.png"))
LASER_BLUE = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
LASER_YELLOW = pygame.image.load(
    os.path.join("assets", "pixel_laser_yellow.png"))

# BACKGROUND IMAGE
bg_image = pygame.image.load(os.path.join("assets", "background-black.png"))
BACKGROUND = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (int(self.x), int(self.y)))

    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)
    
class Ship:
    COOL_DOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (int(self.x), int(self.y)))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=health)
        self.ship_img = SPACE_SHIP_YELLOW
        self.laser_img = LASER_YELLOW
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else: 
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (int(self.x), int(self.y + self.ship_img.get_height() + 10), int(self.ship_img.get_width()), 10))
        pygame.draw.rect(window, (0,255,0), (int(self.x), int(self.y + self.ship_img.get_height() + 10), int(self.ship_img.get_width() * (self.health/self.max_health)), 10))


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

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 15, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

def main():
    run = 1
    FPS = 60
    level = 1
    lives = 5
    font_family = "comicsans"
    font_size = 25
    main_font = pygame.font.SysFont(font_family, font_size)
    lost_font = pygame.font.SysFont(font_family, font_size)

    lost = False
    lost_count = 0

    enemies = []

    wave_level = 5

    enemy_vel = 1

    player_vel = 5

    laser_vel = 5

    player = Player(WIDTH/2, HEIGHT - 115)

    clock = pygame.time.Clock()

    def redraw_window():
        # BG
        WIN.blit(BACKGROUND, (0, 0))

        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        levels_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render('Busted.!!!', 1, (255, 255, 255))
            WIN.blit (lost_label,(int(WIDTH/2 - lost_label.get_width()/2), int(HEIGHT/2 - lost_label.get_height()/2)))

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
                #health = 100 if color == "green" else 200 if color == "blue" else 300
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

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
            
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    font_family = "comicsans"
    font_size = 50
    title_font = pygame.font.SysFont(font_family, font_size)
    run = True
    while run:
        WIN.blit(BACKGROUND, (0, 0))
        title_label = title_font.render("Press mouse button to begin...", 1, (255,255,255))
        WIN.blit(title_label, (int(WIDTH/2 - title_label.get_width()/2), int(HEIGHT/2 - title_label.get_height()/2)))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

if __name__ == '__main__':
    main_menu()