import os

import pygame

FPS = 60
WIDTH, HEIGHT = 640, 480
FONT_FAMILY = "comicsans"

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")
TO_ASSETS = "assets"

# ENIMY SHIP
SPACE_SHIP_RED = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
SPACE_SHIP_GREEN = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
SPACE_SHIP_BLUE = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# PLAYER SHIP
SPACE_SHIP_YELLOW = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# LASERS
LASER_RED = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
LASER_GREEN = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
LASER_BLUE = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
LASER_YELLOW = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# BACKGROUND IMAGE
bg_image = pygame.image.load(os.path.join("assets", "background-black.png"))
BACKGROUND = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
